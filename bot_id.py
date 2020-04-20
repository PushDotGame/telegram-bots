import conf.bot as be
import libs.shell as shell
from libs.MQBot import MQBot
from telegram import ParseMode
from telegram.ext import (Updater, Filters, CommandHandler, MessageHandler)


def private_command_start(update, context):
    update.message.reply_text(
        text='Add this bot to a group or a channel as administrator,'
             '\n\nthen send `/id`, I\'ll answer.'
             '\n\nIn a channel, please send `id?`',
        reply_to_message_id=update.effective_message.message_id,
    )


def private_command_id(update, context):
    update.message.reply_text(
        text='`{}`'.format(str(update.effective_user)),
        reply_to_message_id=update.effective_message.message_id,
    )


def group_command_id(update, context):
    update.message.reply_text(
        text='Chat\n`{}`\n\nUser\n`{}`'.format(
            update.effective_chat,
            update.effective_user,
        ),
        reply_to_message_id=update.effective_message.message_id,
    )


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
            text='This {} ID\n`{}`'.format(
                update.effective_chat.type,
                update.effective_chat.id,
            ),
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
