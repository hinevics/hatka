import pandas as pd
from dagster import asset, get_dagster_logger
# from sklearn.model_selection import train_test_split
# from catboost import Pool, CatBoostRegressor
# from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


@asset
def test_print() -> None:
    print('TEST')


@asset
def as_1() -> dict:
    return {'1': 1}


@asset
def as_2() -> dict:
    return {'2': 2}


@asset
def as_3(as_2: dict, as_1: dict) -> None:
    as_2.update(as_1)
    return as_2
