import os
import dotenv
import conf.bot as be
import libs.shell as shell
from libs.MQBot import MQBot
from telegram import ParseMode
from telegram.ext import (Updater, Filters, CommandHandler, MessageHandler)

# load: `.bot.session_name`
dotenv.load_dotenv(dotenv_path=os.path.join(be.ENV_DIR, '.bot.{}'.format(be.BOT_SESSION_NAME)))
FORWARD_CHAT_ID = os.getenv("FORWARD_CHAT_ID")


def private_command_start(update, context):
    update.message.reply_text(
        text='Hi, I can forward your every message to @julia4pr',
        reply_to_message_id=update.effective_message.message_id,
        # parse_mode=ParseMode.MARKDOWN,
        # disable_web_page_preview=True,
    )


def private_message(update, context):
    update.effective_message.forward(FORWARD_CHAT_ID)
    update.message.reply_text(
        text='`Forwarded.`',
        reply_to_message_id=update.effective_message.message_id,
        # parse_mode=ParseMode.MARKDOWN,
        # disable_web_page_preview=True,
    )


def main():
    # bot
    bot = MQBot(token=be.BOT_TOKEN)

    # init python-telegram-bot: updater and dispatcher
    updater = Updater(
        bot=bot,
        use_context=True,
        request_kwargs=be.REQUEST_KWARGS,
    )

    # dispatcher
    dp = updater.dispatcher

    # `/start`
    dp.add_handler(CommandHandler(
        filters=Filters.private,
        command='start',
        callback=private_command_start,
    ))

    # private message
    dp.add_handler(MessageHandler(
        filters=Filters.private & (~ Filters.sticker),
        callback=private_message,
    ))

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
        updater.stop()
        print('updater stopped.')
        return

    # exit
    def xx():
        stop()
        exit('Goodbye.')
        return

    start()

    if be.DEBUG_MODE:
        shell.embed()


if __name__ == "__main__":
    main()
