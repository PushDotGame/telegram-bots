import os
import sys
from libs.config import *
from libs import functions as lf

# bot session name
if len(sys.argv) < 2:
    exit('Please run `python3 {} <bot_session_name>`'.format(sys.argv[0]))
BOT_SESSION_NAME = sys.argv[1].lower()

# language
LANGUAGE = 'en-US'
if len(sys.argv) > 2:
    LANGUAGE = sys.argv[2]

# server
SERVER_LISTEN = cfg.get('deploy', 'LISTEN') or '0.0.0.0'
SERVER_DOMAIN = cfg.get('deploy', 'SERVER_DOMAIN')
SERVER_PORT = cfg.getint('deploy', 'SERVER_PORT') or 8443

# cert
PATH_TO_KEY = os.path.join(CERT_DIR, '{}_private.key'.format(SERVER_DOMAIN))
PATH_TO_CERT = os.path.join(CERT_DIR, '{}_cert.pem'.format(SERVER_DOMAIN))

# proxy
PROXY_URL = cfg.get(BOT_SESSION_NAME, 'PROXY_URL') or None
REQUEST_KWARGS = None
if PROXY_URL:
    REQUEST_KWARGS = {
        'proxy_url': PROXY_URL
    }

# bot dir
BOT_DATA_DIR = lf.touch_dirs(
    cfg.get(BOT_SESSION_NAME, 'DATA_DIR') or os.path.join(DATA_DIR, BOT_SESSION_NAME)
)
BOT_LOG_DIR = lf.touch_dirs(
    cfg.get(BOT_SESSION_NAME, 'LOG_DIR') or os.path.join(BOT_DATA_DIR, 'logs')
)
BOT_CACHE_DIR = lf.touch_dirs(
    cfg.get(BOT_SESSION_NAME, 'CACHE_DIR') or os.path.join(BOT_DATA_DIR, 'cache')
)

# bot
BOT_TOKEN = cfg.get(BOT_SESSION_NAME, 'TOKEN')
BOT_PORT = int(cfg.get(BOT_SESSION_NAME, 'PORT') or SERVER_PORT)
BOT_ID = int(BOT_TOKEN.split(':')[0])
BOT_URL_PATH = '/{}'.format(BOT_ID)
BOT_OWNER_ID = cfg.getint(BOT_SESSION_NAME, 'OWNER_ID')

# webhook
BOT_WEBHOOK_URL = 'https://{domain}:{port}/{bot_id}'.format(
    domain=SERVER_DOMAIN,
    port=SERVER_PORT,
    bot_id=BOT_ID
)
