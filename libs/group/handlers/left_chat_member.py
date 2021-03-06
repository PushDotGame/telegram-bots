from telegram.ext import (Dispatcher, MessageHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs import CacheORM as Cache


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        MessageHandler(
            filters=Filters.status_update.left_chat_member,
            callback=_left_chat_member,
        )
    )


@run_async
def _left_chat_member(update, context):
    # cached kicked user id
    key = '{chat_id}_kick_user_id'.format(chat_id=update.effective_chat.id)
    user_id = Cache.get(key)

    if user_id != update.effective_message.left_chat_member.id:
        update.effective_message.delete()
