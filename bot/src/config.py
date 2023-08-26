import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
PATH_TEST_FLAT = os.getenv("PATH_TEST_FLAT")
