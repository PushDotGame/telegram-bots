import libs.settings as settings
import libs.shell as shell
from libs.MQBot import MQBot
from libs.group import handlers
from telegram.ext import Updater


def main():
    # bot
    bot = MQBot(token=settings.BOT_TOKEN)

    # updater
    updater = Updater(
        bot=bot,
        use_context=True,
        request_kwargs=settings.REQUEST_KWARGS,
    )

    # dispatcher
    dp = updater.dispatcher

    # private: `/start`
    handlers.private_command_start.attach(dp)

    # group: `/serve`
    handlers.group_command_serve.attach(dp)

    # group: `/kick`
    handlers.group_command_kick.attach(dp)

    # group: text, new, left
    handlers.group_text.attach(dp)
    handlers.new_chat_members.attach(dp)
    handlers.left_chat_member.attach(dp)

    def start():
        updater.start_webhook(
            listen=settings.LISTEN,
            port=settings.BOT_PORT,
            url_path=settings.BOT_ID,
            key=settings.PATH_TO_KEY,
            cert=settings.PATH_TO_CERT,
            webhook_url=settings.WEBHOOK_URL,
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

    if settings.DEBUG:
        shell.embed()


if __name__ == "__main__":
    main()
