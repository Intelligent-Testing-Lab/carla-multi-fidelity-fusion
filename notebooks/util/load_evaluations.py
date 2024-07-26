import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from pathlib import Path
import numpy as np
import seaborn as sns
from itertools import batched

DEFAULT_DIR = "data/evaluation/benchmarking/default"


def extract_evaluation_file(file_path: Path) -> pd.DataFrame:

    data = {}

    # extract data from path
    match file_path.parts:
        case [*_, rep_id, _, _]:

            data['rep'] = rep_id[-1]
            path_params = dict(batched(file_path.stem.split("_"), n=2))
            data.update(path_params)

        case _:
            print(f"File path didn't match the pattern")

    # extract data from file
    with open(file_path, "r") as f:
        content = json.load(f)

    data['records'] = content['_checkpoint']['records']
    df = pd.DataFrame(data)
    return df


def transform_evaluation_df(df: pd.DataFrame) -> pd.DataFrame:

    df = df.reset_index(drop=True)
    # unpack records
    record_df = pd.json_normalize(df['records'])
    # concatenate records data
    df = pd.concat([df, record_df],  axis=1)

    # drop original column
    df = df.drop('records', axis=1)

    # drop infractions columns

    # remove prefixes from column name
    df.columns = df.columns.str.removeprefix('meta.')
    df.columns = df.columns.str.removeprefix('scores.')
    df['driving_score'] = df['score_composed'] / 100
    df = df.rename(columns={"index": "route_index"})

    df = df.set_index(['rep', 'fps', 'highquality', 'route_index'])
    df = df.sort_index()
    return df


def load_evaluation_df(eval_dir: str = DEFAULT_DIR) -> pd.DataFrame:
    eval_dir_path = Path(eval_dir)

    if not eval_dir_path.exists():
        raise FileNotFoundError

    file_dfs = []
    for file_path in eval_dir_path.glob("./rep*/*/*.json"):
        file_dfs.append(extract_evaluation_file(file_path))

    df = pd.concat(file_dfs)
    df = transform_evaluation_df(df)
    return df


if __name__ == "__main__":
    df = load_evaluation_df()
    print(df)
