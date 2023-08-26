import pickle
import random
from config import PATH_TEST_FLAT


def get_test_flat():
    with open(PATH_TEST_FLAT, mode='rb') as file:
        data = pickle.load(file)
    k = list(data.keys())
    return data[k[random.randint(0, len(k) - 1)]]
