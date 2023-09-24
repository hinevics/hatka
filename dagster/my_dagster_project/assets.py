import pandas as pd
from dagster import asset, get_dagster_logger
# from sklearn.model_selection import train_test_split
# from catboost import Pool, CatBoostRegressor
# from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


@asset
def test_print() -> None:
    print('TEST')
