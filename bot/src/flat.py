import pickle
import random
import pandas as pd

from config import PATH_TEST_FLAT, PATH_DATA


def load_data(path: str):
    pass


def get_test_flat():
    with open(PATH_TEST_FLAT, mode='rb') as file:
        data = pickle.load(file)
    k = list(data.keys())
    flat_id = k[random.randint(0, len(k) - 1)]

    return {
        "id": flat_id,
        "title": data[flat_id]["title"],
        "href": data[flat_id]["href"],
        "adres": data[flat_id]["adres"],
        "rooms": data[flat_id].get('Количество комнат', None),
        "price": data[flat_id]["price"]
    }


def get_first_flat() -> dict:
    """Функция возвращает рандомную квартиру
    """
    data = pd.read_pickle(PATH_DATA)
    random_index = list(data.index)[random.randint(0, len(data.index) - 1)]
    answer = data.loc[random_index].to_dict()
    answer['loc'] = random_index
    return answer


def find_flat(index: int) -> pd.Series:
    """Функция для поиска квартиры в списке квартир

    Args:
        index (int): индекс квартиры

    Returns:
        pd.Series: _description_
    """
    data = pd.read_pickle(PATH_DATA)
    answer = data.loc[index]
    return answer


def predict_like_flat(index: int) -> dict:
    """Функция выполняет предсказание если пользователь поставил лайк.
    Тогда вектор квартиры X_liked
    """

    data = find_flat(index)
    vector = data.vectors
    index_predicted = predict()



def predict_diselike_flat(index: int) -> dict:
    data = find_flat(index)
    print(data)