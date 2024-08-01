import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from pathlib import Path
import numpy as np
import seaborn as sns
from itertools import batched

DEFAULT_DIR = Path("data/evaluation")
DEFAULT_BENCHMARKING_DIR = DEFAULT_DIR / "benchmarking" / "default"
DEFAULT_RANDOMSEARCH_DIR = DEFAULT_DIR / "random_search"


def _read_file_records(file_path: Path) -> list:
    # extract data from file
    with open(file_path, "r") as f:
        content = json.load(f)

    return content['_checkpoint']['records']


def _read_benchmark_file(file_path: Path) -> pd.DataFrame:

    data = {}

    # extract data from path
    match file_path.parts:
        case [*_, rep_id, _, _]:

            data['rep'] = rep_id[-1]
            path_params = dict(batched(file_path.stem.split("_"), n=2))
            data.update(path_params)

        case _:
            print(f"File path didn't match the pattern")

    data['records'] = _read_file_records(file_path)
    df = pd.DataFrame(data)
    return df


def _calculate_benchmark_dscore_error(df: pd.DataFrame) -> pd.DataFrame:
    oracle_df = df.xs((20, "True"), level=[
                      'fps', 'highquality'], drop_level=False).sort_index()

    oracle_dscore_vec = oracle_df.groupby(
        'route_index')['driving_score'].mean()
    df['driving_score_error'] = (df['driving_score'] - oracle_dscore_vec).abs()

    return df


def _transform_df(df: pd.DataFrame) -> pd.DataFrame:

    df = df.reset_index(drop=True)
    # unpack records
    record_df = pd.json_normalize(df['records'])
    # concatenate records data
    df = pd.concat([df, record_df],  axis=1)

    # drop original column
    df = df.drop('records', axis=1)

    # remove prefixes from column name
    df.columns = df.columns.str.removeprefix('meta.')
    df.columns = df.columns.str.removeprefix('scores.')
    df['driving_score'] = df['score_composed'] / 100
    df = df.rename(columns={"index": "route_index"})

    df['fps'] = pd.to_numeric(df['fps'])

    return df


def load_benchmark_df(eval_dir_path: Path | str = DEFAULT_BENCHMARKING_DIR) -> pd.DataFrame:
    eval_dir_path = Path(eval_dir_path)

    if not eval_dir_path.exists():
        raise FileNotFoundError

    file_dfs = []
    for file_path in eval_dir_path.glob("./rep*/**/*.json"):
        file_dfs.append(_read_benchmark_file(file_path))

    df = pd.concat(file_dfs)
    df = _transform_df(df)
    df = df.set_index(['fps', 'highquality', 'rep', 'route_index'])
    df = df.sort_index()

    df = _calculate_benchmark_dscore_error(df)
    return df


def _read_rs_file(file_path: Path):
    data = {}

    # extract data from path
    match file_path.parts:
        case [*_, ("rs_v3" | "rs_v4") as batch, rep, _, it, _] if "it" in it:

            data['rep'] = int(rep)
            data['it'] = int(it[2:])
            if "4" in batch:
                data['rep'] += 10

            stem_params = dict(batched(file_path.stem.split("_"), n=2))
            data.update(stem_params)

        case _:
            return None

    # there is only one so take that
    data['records'] = _read_file_records(file_path)[0]
    return data


def load_rs_df(rs_dir_path: Path = DEFAULT_RANDOMSEARCH_DIR) -> pd.DataFrame:
    rs_dir_path = Path(rs_dir_path)

    if not rs_dir_path.exists():
        raise FileNotFoundError

    file_data_list = []
    for file_path in rs_dir_path.glob("./**/*.json"):
        file_data = _read_rs_file(file_path)
        if file_data:
            file_data_list.append(file_data)

    df = pd.DataFrame(file_data_list)
    df = _transform_df(df)
    df = df.set_index(['fps', 'highquality', 'rep', 'it',]).sort_index()
    return df


if __name__ == "__main__":

    df = load_benchmark_df()
    print(df)
    df = load_rs_df()
    print(f'{df}')
