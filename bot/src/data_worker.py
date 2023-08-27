"Модуль для работы с датой"

from typing import Any
import csv

from config import PATH_DATA_USER, PATH_DATA_USERACTION


# header_action = ["user_name", "action", 'dtime']
# header_user_data = ["user_name", "flat_id", "like", "dtime"]


def update_action(data: list[tuple[Any]]):
    """Функция для обновления данных по действиям user'a

    Args:
        data (list[tuple[Any]]): Набор действий
    """

    with open(PATH_DATA_USERACTION, mode="a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        # csvwriter.writerow(header_action)

        for row in data:
            csvwriter.writerow(row)


def update_user(data: list[tuple[Any]]):
    """Функция для обновления данных по user

    Args:
        data (list[tuple[Any]]): Набор данных по предпочтению
    """
    with open(PATH_DATA_USER, mode="a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        # csvwriter.w(header_user_data)

        for row in data:
            csvwriter.writerow(row)
