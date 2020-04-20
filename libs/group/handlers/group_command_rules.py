from telegram.ext import (Dispatcher, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.group.kvs import kvs
from . import functions as hf
from conf import bot as be
from libs.FileCache import FileCache

# file cache
FC = FileCache(be.BOT_CACHE_DIR)


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        CommandHandler(
            command='rule',
            filters=Filters.group,
            callback=_group_command_rules,
        )
    )

    dispatcher.add_handler(
        CommandHandler(
            command='rules',
            filters=Filters.group,
            callback=_group_command_rules,
        )
    )


@run_async
def _group_command_rules(update, context):
    update.message.reply_text(
        text=kvs['rules'],
    )
