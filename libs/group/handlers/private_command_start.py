from telegram.ext import (Dispatcher, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.group.kvs import kvs

COMMAND = 'start'


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        CommandHandler(
            command=COMMAND,
            filters=Filters.private,
            callback=_private_command_start,
        )
    )


@run_async
def _private_command_start(update, context):
    update.message.reply_text(
        text=kvs['command_start'].format(
            owner_name=kvs['owner_name'],
            owner_username=kvs['owner_username'],
        ),
        reply_to_message_id=update.effective_message.message_id,
        disable_web_page_preview=True,
    )
