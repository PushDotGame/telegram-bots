import os
import dotenv
from libs import settings

# load: `.bot.session_name`
dotenv.load_dotenv(dotenv_path=os.path.join(settings.ENV_DIR, '.bot.{}'.format(settings.BOT_SESSION_NAME)))

BOT_OWNER_ID = int(os.getenv("OWNER_ID"))
FULL_NAME_TOO_LONG = int(os.getenv("FULL_NAME_TOO_LONG") or 30)
SLEEP_SECONDS = int(os.getenv("SLEEP_SECONDS") or 60)
REMOVE_FOOTPRINT = os.getenv("REMOVE_FOOTPRINT", 'False').lower() == 'true'
