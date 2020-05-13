import os
from configparser import ConfigParser
from libs import functions as lf

# dir
BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))
CONF_DIR = os.path.join(BASE_DIR, 'conf')
CONTRACTS_DIR = os.path.join(BASE_DIR, 'contracts')
LOCALE_DIR = lf.touch_dirs(os.path.join(BASE_DIR, 'locale'))

# config.ini
cfg = ConfigParser()
cfg.read(os.path.join(CONF_DIR, 'config.ini'))

# deploy
DEBUG_MODE = cfg.getboolean('deploy', 'DEBUG_MODE')

# dirs
CERT_DIR = lf.touch_dirs(cfg.get('deploy', 'CERT_DIR') or os.path.join(BASE_DIR, '.cert'))
DATA_DIR = lf.touch_dirs(cfg.get('deploy', 'DATA_DIR') or os.path.join(BASE_DIR, '.data'))
DOG_DIR = lf.touch_dirs(cfg.get('deploy', 'DOG_DIR') or os.path.join(DATA_DIR, 'dog'))

# web3
WEB3_HTTP_PROVIDER = cfg.get('web3', 'HTTP_PROVIDER')

# game
GAME_ADDRESS = cfg.get('game', 'GAME_ADDRESS') or '0x1234567B172f040f45D7e924C0a7d088016191A6'
READER_A_ADDRESS = cfg.get('game', 'READER_A_ADDRESS') or '0x123A1eef39875D6009F66211d80E726067Ae74b6'
READER_B_ADDRESS = cfg.get('game', 'READER_B_ADDRESS') or '0x123B2B91523F90F69C60a93E1161e7f1783C06a8'

get = cfg.get
getboolean = cfg.getboolean
getint = cfg.getint
getfloat = cfg.getfloat
