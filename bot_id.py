from libs import shell
from libs import config_bot as config
from libs.MQBot import MQBot
from telegram.ext import (Updater, Filters, CommandHandler, MessageHandler)


def private_command_start(update, context):
    update.message.reply_text('Add this bot to a group or a channel as administrator,'
                              '\n\nthen send `/id`, I\'ll answer.'
                              '\n\nIn a channel, please send `id?`')


def private_command_id(update, context):
    update.message.reply_text('`{}`'.format(str(update.effective_user)))


def group_command_id(update, context):
    update.message.reply_text('Chat\n`{}`\n\nUser\n`{}`'.format(update.effective_chat,
                                                                update.effective_user))


def channel_id(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='This channel ID\n`{}`'.format(update.effective_chat.id),
    )


def new_chat_members(update, context):
    # bot joined
    bot_joined = False
    for u in update.message.new_chat_members:
        if u.id == context.bot.id:
            bot_joined = True

    if bot_joined:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='This {} ID\n`{}`'.format(update.effective_chat.type,
                                           update.effective_chat.id),
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

    # private `/start`
    dp.add_handler(CommandHandler(
        filters=Filters.private,
        command='start',
        callback=private_command_start,
    ))

    # private `/id`
    dp.add_handler(CommandHandler(
        filters=Filters.private,
        command='id',
        callback=private_command_id,
    ))

    # group `/id`
    dp.add_handler(CommandHandler(
        filters=Filters.group,
        command='id',
        callback=group_command_id,
    ))

    # channel `id?`
    dp.add_handler(MessageHandler(
        filters=Filters.update.channel_posts & Filters.regex(r'(^id\?$)'),
        callback=channel_id,
    ))

    # when join a group
    dp.add_handler(MessageHandler(
        filters=Filters.status_update.new_chat_members,
        callback=new_chat_members,
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
