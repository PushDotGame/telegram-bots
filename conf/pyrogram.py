import sys
from libs.settings import *
from decimal import Decimal

dotenv.load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

PYROGRAM_API_ID = os.getenv("PYROGRAM_API_ID")
PYROGRAM_API_HASH = os.getenv("PYROGRAM_API_HASH")
PYROGRAM_APP_VERSION = os.getenv("PYROGRAM_APP_VERSION")
PYROGRAM_DEVICE_MODEL = os.getenv("PYROGRAM_DEVICE_MODEL")
PYROGRAM_SYSTEM_VERSION = os.getenv("PYROGRAM_SYSTEM_VERSION")

# session name
if len(sys.argv) < 2:
    exit('Please run `python3 {} <session_name>`'.format(sys.argv[0]))
SESSION_NAME = sys.argv[1]

TG_DATA_DIR = fn.touch_dirs(os.getenv("TG_CACHE_DIR", os.path.join(DATA_DIR, 'pyrogram')))

PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = int(os.getenv("PROXY_PORT", 1080))
PROXY = None

if PROXY_HOST:
    PROXY = dict(
        hostname=PROXY_HOST,
        port=PROXY_PORT
    )

DECIMAL = Decimal(os.getenv("DECIMAL", '0.0000'))
