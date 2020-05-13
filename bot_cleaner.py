import libs.shell as shell
from libs import config_bot as config
from libs.MQBot import MQBot
from libs.cleaner import handlers
from libs.CleanerORM import *
from telegram.ext import Updater


def main():
    # bot
    bot = MQBot(token=config.BOT_TOKEN)

    # updater
    updater = Updater(
        bot=bot,
        use_context=True,
        request_kwargs=config.REQUEST_KWARGS,
    )

    # dispatcher
    dp = updater.dispatcher

    # private: `/start`
    handlers.private_command_start.attach(dp)

    # group: `/clean`
    handlers.group_command_clean.attach(dp)

    # group: new, left
    handlers.new_chat_members.attach(dp)
    handlers.left_chat_member.attach(dp)

    def start():
        updater.start_webhook(
            listen=config.SERVER_LISTEN,
            port=config.BOT_PORT,
            url_path=config.BOT_URL_PATH,
            key=config.PATH_TO_KEY,
            cert=config.PATH_TO_CERT,
            webhook_url=config.BOT_WEBHOOK_URL,
        )
        print('updater started.')
        return

    def stop():
        bot.stop_mq()
        updater.stop()
        print('updater stopped.')
        exit('Goodbye.')
        return

    start()

    if config.DEBUG_MODE:
        shell.embed()


if __name__ == "__main__":
    with db_logger:
        db_logger.create_tables([Chat, User, ChatUser])
    main()
