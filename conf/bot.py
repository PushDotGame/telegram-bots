import sys
from libs.settings import *

# local
LISTEN = os.getenv("LISTEN", '0.0.0.0')
SERVER_DOMAIN = os.getenv("SERVER_DOMAIN")
SERVER_PORT = int(os.getenv("SERVER_PORT") or 8443)
PATH_TO_KEY = os.path.join(CERT_DIR, '{}_private.key'.format(SERVER_DOMAIN))
PATH_TO_CERT = os.path.join(CERT_DIR, '{}_cert.pem'.format(SERVER_DOMAIN))

# proxy
PROXY_URL = os.getenv("PROXY_URL", None)
REQUEST_KWARGS = None
if PROXY_URL:
    REQUEST_KWARGS = {
        'proxy_url': PROXY_URL
    }

# bot session name
BOT_SESSION_NAME = os.getenv("BOT_SESSION_NAME", None)
if BOT_SESSION_NAME is None:
    if len(sys.argv) < 2:
        exit('Please run `python3 {} <bot_session_name>`'.format(sys.argv[0]))
    BOT_SESSION_NAME = sys.argv[1].lower()

# bot config
ENV_DIR = fn.touch_dirs(os.getenv("ENV_DIR") or DATA_DIR)
dotenv.load_dotenv(dotenv_path=os.path.join(ENV_DIR, '.bot.{}'.format(BOT_SESSION_NAME)))

BOT_DATA_DIR = fn.touch_dirs(os.getenv("DATA_DIR") or os.path.join(DATA_DIR, BOT_SESSION_NAME))
BOT_LOG_DIR = fn.touch_dirs(os.getenv("LOG_DIR") or os.path.join(BOT_DATA_DIR, 'logs'))
BOT_CACHE_DIR = fn.touch_dirs(os.getenv("CACHE_DIR") or os.path.join(BOT_DATA_DIR, 'cache'))

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PORT = int(os.getenv("BOT_PORT") or SERVER_PORT)
BOT_ID = fn.get_id_from_bot_token(BOT_TOKEN)

# webhook
WEBHOOK_URL = 'https://{domain}:{port}/{bot_id}'.format(
    domain=SERVER_DOMAIN,
    port=SERVER_PORT,
    bot_id=BOT_ID
)
