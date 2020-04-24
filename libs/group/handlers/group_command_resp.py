# coding=utf-8

import os
import time
import codecs
import random
from telegram.ext import (Dispatcher, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.group.kvs import kvs
from . import functions as hf
from conf import bot as be
from libs import functions as lf
from libs.FileCache import FileCache

# file cache
FC = FileCache(be.BOT_CACHE_DIR)


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        CommandHandler(
            command='resp',
            filters=Filters.group,
            callback=_group_command_resp,
        )
    )


@run_async
def _group_command_resp(update, context):
    if len(context.args) > 0:
        chat_admin = hf.get_admin_chat(update)
        if chat_admin is None:
            return

        key = context.args[0]

        path_to_file = os.path.join(os.path.join(be.BOT_DATA_DIR, 'resp'), '{}.md'.format(key))

        if not os.path.exists(path_to_file):
            update.message.reply_text(
                text='`{}`\n\ndoes not exist.'.format(key),
                disable_web_page_preview=True,
            )
            return

        with codecs.open(path_to_file, 'r', encoding='utf-8') as f:
            content = f.read().format(
                project_name=kvs['project_name'],
                base_url=kvs['base_url'],
                key=kvs['key'],
                owner_name=kvs['owner_name']
            )

            paras = lf.list2solid(content.split('/-/'))

        i = 0
        for para in paras:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=para,
                disable_web_page_preview=True,
            )

            i += 1

            if i % 2 > 0:
                time.sleep(max(3, int(len(para) / 19)))
            else:
                time.sleep(random.randint(10, 15))
