from telegram.ext import (Dispatcher, MessageHandler, Filters)
from telegram.ext.dispatcher import run_async


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        MessageHandler(
            filters=Filters.status_update.left_chat_member,
            callback=_left_chat_member,
        )
    )


@run_async
def _left_chat_member(update, context):
    update.effective_message.delete()
