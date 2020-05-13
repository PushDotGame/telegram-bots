from libs import config_bot as config
from libs import shell
from libs.MQBot import MQBot
from telegram.ext import (Updater, Filters, CommandHandler, MessageHandler)

FORWARD_CHAT_ID = config.getint(config.BOT_SESSION_NAME, 'FORWARD_CHAT_ID')


def private_command_start(update, context):
    update.message.reply_text(
        text='Hi, I can forward your every message to @julia4pr',
        reply_to_message_id=update.effective_message.message_id
    )


def private_message(update, context):
    update.effective_message.forward(FORWARD_CHAT_ID)
    update.message.reply_text(
        text='`Forwarded.`',
        reply_to_message_id=update.effective_message.message_id
    )


def main():
    # bot
    bot = MQBot(token=config.BOT_TOKEN)

    # init python-telegram-bot: updater and dispatcher
    updater = Updater(
        bot=bot,
        use_context=True,
        request_kwargs=config.REQUEST_KWARGS,
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
        updater.start_webhook(listen=config.SERVER_LISTEN,
                              port=config.BOT_PORT,
                              url_path=config.BOT_URL_PATH,
                              key=config.PATH_TO_KEY,
                              cert=config.PATH_TO_CERT,
                              webhook_url=config.BOT_WEBHOOK_URL)
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
    main()
