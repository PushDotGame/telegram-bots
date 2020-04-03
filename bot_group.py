import libs.settings as settings
import os
import dotenv
import telegram
import importlib
import libs.shell as shell

from libs.MQBot import MQBot
from libs.FileCache import FileCache
from presets.group_tmpl import text_values as tv

from telegram.ext import (Updater, Filters, CommandHandler, MessageHandler)

# text values
tv_customize = importlib.import_module('presets.bot_{}'.format(settings.BOT_SESSION_NAME))
tv.update(tv_customize.text_values)

# file cache
FC = FileCache(settings.BOT_CACHE_DIR)

# load: `.bot.session_name`
dotenv.load_dotenv(dotenv_path=os.path.join(settings.ENV_DIR, '.bot.{}'.format(settings.BOT_SESSION_NAME)))

OWNER_ID = int(os.getenv("OWNER_ID"))
FULL_NAME_TOO_LONG = int(os.getenv("FULL_NAME_TOO_LONG") or 30)


def private_command_start(update, context):
    update.message.reply_text(
        text=tv['command_start'].format(owner_name=tv['owner_name'], owner_username=tv['owner_username']),
        reply_to_message_id=update.effective_message.message_id,
    )


def group_text(update, context):
    update.message.reply_text(
        text='text',
        reply_to_message_id=update.effective_message.message_id,
    )
    pass


# def private_message(update, context):
#     message = update.message.reply_text(
#         text=tv['private_message'],
#         reply_to_message_id=update.effective_message.message_id,
#     ).result()
#
#     if message:
#         key = '{}_message'.format(update.effective_chat.id)
#
#         previous_id = FC.get(key)
#         FC.put(key, message.message_id)
#
#         if previous_id:
#             context.bot.delete_message(
#                 chat_id=update.effective_chat.id,
#                 message_id=previous_id,
#             )


def new_chat_members(update, context):
    """When new member(s) joined a group, send welcome text, and remove the previous"""

    # delete notification message, if a full name is too long
    _delete_notification_if_full_name_too_long(update.message.new_chat_members, update.effective_message)

    # # when bot joined
    # for member in update.message.new_chat_members:
    #     if member.id == context.bot.id:
    #         update.message.reply_text(text='Hi')
    #         break

    # new members
    members = list()
    for member in update.message.new_chat_members:
        if len(member.full_name) <= FULL_NAME_TOO_LONG:
            members.append(member.mention_markdown())

    # send welcome
    message = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=tv['welcome'].format(
            members=', '.join(members),
            rules=tv['rules']
        ),
    ).result()

    # cache, then delete the previous
    if message:
        key = '{}_welcome'.format(update.effective_chat.id)

        previous_id = FC.get(key)
        FC.put(key, message.message_id)

        if previous_id:
            context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=previous_id,
            )


def left_chat_member(update, context):
    update.effective_message.delete()
    # _delete_notification_if_full_name_too_long([update.message.left_chat_member], update.effective_message)


def _delete_notification_if_full_name_too_long(members, message: telegram.Message):
    for member in members:
        if len(member.full_name) > FULL_NAME_TOO_LONG:
            message.delete()


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

    # `/start`
    dp.add_handler(CommandHandler(
        filters=Filters.private,
        command='start',
        callback=private_command_start,
    ))

    # # private message
    # dp.add_handler(MessageHandler(
    #     filters=Filters.private & (~ Filters.sticker),
    #     callback=private_message,
    # ))

    # new_chat_members
    dp.add_handler(MessageHandler(
        filters=Filters.status_update.new_chat_members,
        callback=new_chat_members,
    ))

    # left_chat_member
    dp.add_handler(MessageHandler(
        filters=Filters.status_update.left_chat_member,
        callback=left_chat_member,
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
        bot.stop_mq()
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
