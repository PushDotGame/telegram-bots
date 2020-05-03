from telegram.ext import (Dispatcher, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.FileCache import FileCache
from libs import settings
from libs.group.send_status import send_status

# file cache
FC = FileCache(settings.DOG_DIR)


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        CommandHandler(
            command='game',
            filters=Filters.group,
            callback=_group_command_game,
        )
    )


@run_async
def _group_command_game(update, context):
    send_status(update, context, reply=True, part2=True)
