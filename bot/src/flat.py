import pickle
import random

from config import PATH_TEST_FLAT


def load_model(path: str):
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
