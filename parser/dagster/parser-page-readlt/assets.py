from dagster import asset
# from sklearn.model_selection import train_test_split
# from catboost import Pool, CatBoostRegressor
# from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
# from parser.src import main as parser
from src import main as parser

@asset
def start_read_config() -> dict:
    print('------parser')
    print(parser)
    return {'config': 111}


@asset
def as_1(start_read_config: dict) -> dict:
    start_read_config.update({'1': 111})
    return start_read_config


@asset
def as_2() -> dict:
    return {'2': 2}


@asset
def as_3(as_1: dict, as_2: dict) -> dict:
    as_2.update(as_1)
    print('print parser in as_3')
    # print('--------------------', parser)
    return as_2
