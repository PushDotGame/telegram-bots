import libs.settings as settings
import libs.shell as shell
from telegram import ParseMode
from telegram.ext import (Updater, Defaults, Filters, CommandHandler, MessageHandler)


def private_command_start(update, context):
    update.message.reply_text(
        text='Hi, I can forward your every message to @julia4pr',
        reply_to_message_id=update.effective_message.message_id,
    )


def private_message(update, context):
    update.effective_message.forward(settings.FORWARD_CHAT_ID)
    update.message.reply_text(
        text='`Forwarded.`',
        reply_to_message_id=update.effective_message.message_id,
    )


def main():
    # defaults
    defaults = Defaults(
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )

    # init python-telegram-bot: updater and dispatcher
    updater = Updater(
        token=settings.BOT_TOKEN,
        use_context=True,
        defaults=defaults,
        request_kwargs=settings.REQUEST_KWARGS,
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
        updater.stop()
        print('updater stopped.')
        return

    # exit
    def xx():
        stop()
        exit('Goodbye.')
        return

    start()
    shell.embed()


if __name__ == "__main__":
    main()
