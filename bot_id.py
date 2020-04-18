import libs.settings as settings
import libs.shell as shell
from telegram import ParseMode
from telegram.ext import (Updater, Defaults, Filters, CommandHandler, MessageHandler)


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
    # defaults
    defaults = Defaults(
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
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

    if settings.DEBUG:
        shell.embed()


if __name__ == "__main__":
    main()
