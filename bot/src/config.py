import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
PATH_TEST_FLAT = os.getenv("PATH_TEST_FLAT")
LOG_PATH = os.getenv('LOG_PATH')
LOG_ERROR_PATH = os.getenv('LOG_ERROR_PATH')
PATH_DATA_USER = os.getenv('PATH_DATA_USER')
PATH_DATA_USERACTION = os.getenv("PATH_DATA_USERACTION")
