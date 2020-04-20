import os
import dotenv
from . import functions as fn

BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)

# load .env
dotenv.load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

DEBUG_MODE = os.getenv("DEBUG", 'False').lower() == 'true'
CERT_DIR = fn.touch_dirs(os.getenv("CERT_DIR") or os.path.join(BASE_DIR, '.cert'))
DATA_DIR = fn.touch_dirs(os.getenv("DATA_DIR") or os.path.join(BASE_DIR, '.data'))
