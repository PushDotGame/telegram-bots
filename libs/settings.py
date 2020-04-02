import os
import sys
import dotenv


def _touch(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)
    return path_to_dir


def _bot_id_from_token(token):
    return token.split(':')[0]


BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)

# bot session name
if len(sys.argv) < 2:
    exit('Please run `python3 {} <bot_session_name>`'.format(__file__))
BOT_SESSION_NAME = sys.argv[1].lower()

# global
dotenv.load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

# cert dir
CERT_DIR = _touch(os.getenv("CERT_DIR") or os.path.join(BASE_DIR, '.cert'))

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

# data
DATA_DIR = _touch(os.getenv("DATA_DIR") or os.path.join(BASE_DIR, '.data'))

# bot config
ENV_DIR = _touch(os.getenv("ENV_DIR") or DATA_DIR)
LOG_DIR = _touch(os.getenv("LOG_DIR") or os.path.join(DATA_DIR, BOT_SESSION_NAME))
dotenv.load_dotenv(dotenv_path=os.path.join(ENV_DIR, '.bot.{}'.format(BOT_SESSION_NAME)))

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PORT = int(os.getenv("BOT_PORT") or SERVER_PORT)
BOT_ID = _bot_id_from_token(BOT_TOKEN)

# webhook
WEBHOOK_URL = 'https://{domain}:{port}/{bot_id}'.format(
    domain=SERVER_DOMAIN,
    port=SERVER_PORT,
    bot_id=BOT_ID
)

# forward to
FORWARD_CHAT_ID = os.getenv("FORWARD_CHAT_ID")
