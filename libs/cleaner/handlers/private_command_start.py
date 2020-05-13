from telegram.ext import (Dispatcher, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async

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
    update.message.reply_text('Julia cleaner bot, only work for an inviter.')
