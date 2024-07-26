
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
import pandas as pd
from shapely import LineString
from numpy.linalg import norm

DEFAULT_SCENARIO_PATH = "data/definition/routes_devtest_sliced.xml"


def get_turn_angles(polyline: LineString) -> float:
    coords = np.array(polyline.coords)

    angles = []

    for p0, p1, p2 in zip(coords, coords[1:], coords[2:]):
        # get two vectors from three points
        v1 = p1 - p0
        v2 = p2 - p1
        cos_theta = np.dot(v1, v2) / (norm(v1)*norm(v2))

        # avoiding float points errors
        if cos_theta > 1.0:
            cos_theta = 1.0

        theta = np.rad2deg(np.arccos(cos_theta))

        angles.append(theta)

    # if there was only two points hence no angle return 0
    if not angles:
        return [0.0]

    return angles


# get distance between first and last point in a poly line
def get_straight_distance(polyline: LineString) -> float:
    coords = np.array(polyline.coords)
    return norm(coords[0]-coords[-1])


def get_route_data(route: ET.Element):
    points = [[waypoint.attrib['x'], waypoint.attrib['y'], waypoint.attrib['z']]
              for waypoint in route]

    # convert points to floats
    points = [list(map(float, p)) for p in points]

    ret = {"points": points,
           **route.attrib
           }
    return ret


def transform_scenario_df(df: pd.DataFrame) -> pd.DataFrame:
    # drop duplicate routes
    df = df.drop_duplicates('points')

    # set route's id to be df's index
    df = df.rename(columns={"id": "route_index"})
    df = df.set_index('route_index')

    # count points
    df['n_points'] = df['points'].apply(len)

    # transform points to shapely linestrings to represent polylines
    df['points'] = df['points'].apply(lambda x: LineString(x))

    # from a polyline get a list of turn angles
    df['angles'] = df['points'].apply(get_turn_angles)

    df['length'] = df['points'].apply(lambda x: x.length)
    df['dist'] = df['points'].apply(get_straight_distance)
    df['dist_len_ratio'] = df['dist'] / df['length']

    df['max_angles'] = df['angles'].apply(max)
    df['avg_angles'] = df['angles'].apply(lambda x: sum(x)/len(x))
    df['n_turns'] = df['angles'].apply(
        lambda x: len([angle for angle in x if angle > 30]))

    return df


def load_scenario_df(xml_file: str = DEFAULT_SCENARIO_PATH) -> pd.DataFrame:
    xml_file = Path(xml_file)
    if not xml_file.exists():
        raise FileNotFoundError(xml_file)

    tree = ET.parse(xml_file)

    # Get the root element
    routes = tree.getroot()
    df = pd.DataFrame([get_route_data(route) for route in routes])

    return transform_scenario_df(df)


if __name__ == "__main__":
    df = load_scenario_df()
    print(df)
