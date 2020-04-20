import os
import dotenv
from . import functions as fn

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)
CONTRACTS_DIR = os.path.join(BASE_DIR, 'contracts')

# load .env
dotenv.load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

DEBUG_MODE = os.getenv("DEBUG", 'False').lower() == 'true'
CERT_DIR = fn.touch_dirs(os.getenv("CERT_DIR") or os.path.join(BASE_DIR, '.cert'))
DATA_DIR = fn.touch_dirs(os.getenv("DATA_DIR") or os.path.join(BASE_DIR, '.data'))
DOG_DIR = fn.touch_dirs(os.getenv("DOG_DIR") or os.path.join(os.path.join(BASE_DIR, '.data'), 'dog'))

# web3
WEB3_HTTP_PROVIDER = os.getenv("WEB3_HTTP_PROVIDER")

GAME_ADDRESS = os.getenv("GAME_ADDRESS", '0x1234567B172f040f45D7e924C0a7d088016191A6')
READER_A_ADDRESS = os.getenv("READER_A_ADDRESS", '0x123A1eef39875D6009F66211d80E726067Ae74b6')
READER_B_ADDRESS = os.getenv("READER_B_ADDRESS", '0x123B2B91523F90F69C60a93E1161e7f1783C06a8')
