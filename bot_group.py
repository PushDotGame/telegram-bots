import conf.bot as be
import libs.shell as shell
from libs.MQBot import MQBot
from libs.group import handlers
from telegram.ext import Updater


def main():
    # bot
    bot = MQBot(token=be.BOT_TOKEN)

    # updater
    updater = Updater(
        bot=bot,
        use_context=True,
        request_kwargs=be.REQUEST_KWARGS,
    )

    # dispatcher
    dp = updater.dispatcher

    # private: `/start`
    handlers.private_command_start.attach(dp)

    # group: `/serve`
    handlers.group_command_serve.attach(dp)

    # group: `/kick`
    handlers.group_command_kick.attach(dp)
    handlers.group_command_rules.attach(dp)

    # group: text, new, left
    handlers.group_text.attach(dp)
    handlers.new_chat_members.attach(dp)
    handlers.left_chat_member.attach(dp)

    def start():
        updater.start_webhook(
            listen=be.LISTEN,
            port=be.BOT_PORT,
            url_path=be.BOT_ID,
            key=be.PATH_TO_KEY,
            cert=be.PATH_TO_CERT,
            webhook_url=be.WEBHOOK_URL,
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

    if be.DEBUG_MODE:
        shell.embed()


if __name__ == "__main__":
    main()
