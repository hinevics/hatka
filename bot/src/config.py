import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
PATH_TEST_FLAT = os.getenv("PATH_TEST_FLAT")
LOG_PATH = os.getenv('LOG_PATH')
LOG_ERROR_PATH = os.getenv('LOG_ERROR_PATH')
PATH_DATA_USER = os.getenv('PATH_DATA_USER')
PATH_DATA_USERACTION = os.getenv("PATH_DATA_USERACTION")
PATH_VECTORIZER_MODEL = os.getenv("PATH_VECTORIZER_MODEL")
PATH_PCA_MODEL = os.getenv('PATH_PCA_MODEL')
PATH_NN_MODEL = os.getenv('PATH_NN_MODEL')
PATH_DATA = os.getenv('PATH_DATA')
