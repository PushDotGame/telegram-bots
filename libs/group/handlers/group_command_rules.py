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
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=kvs['rules'],
        disable_web_page_preview=True,
    )
