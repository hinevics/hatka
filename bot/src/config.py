import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
PATH_TEST_FLAT = os.getenv("PATH_TEST_FLAT")
LOG_PATH = os.getenv('LOG_PATH')
LOG_ERROR_PATH = os.getenv('LOG_ERROR_PATH')
PATH_DATA = os.getenv('PATH_DATA')
