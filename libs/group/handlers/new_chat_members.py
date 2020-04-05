import telegram
from telegram.ext import (Dispatcher, MessageHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.group.kvs import kvs
from conf import env
from libs.FileCache import FileCache

# file cache
FC = FileCache(env.settings.BOT_CACHE_DIR)


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        MessageHandler(
            filters=Filters.status_update.new_chat_members,
            callback=_new_chat_members,
        )
    )


def _delete_notification_if_full_name_too_long(members, message: telegram.Message):
    for member in members:
        if len(member.full_name) > env.FULL_NAME_TOO_LONG:
            message.delete()


@run_async
def _new_chat_members(update, context):
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
        if len(member.full_name) <= env.FULL_NAME_TOO_LONG:
            members.append(member.mention_markdown())

    # send welcome
    message = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=kvs['welcome'].format(
            members=', '.join(members),
            rules=kvs['rules']
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
