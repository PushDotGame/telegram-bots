import os
import time
import random
import codecs
import telegram
from telegram.ext import (Dispatcher, MessageHandler, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.group.kvs import kvs
from conf import group_bot
from conf import bot as be
from libs import functions as lf
from libs import CacheORM as Cache
from libs.group.send_status import send_status
from . import functions as hf


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        MessageHandler(
            filters=Filters.status_update.new_chat_members,
            callback=_new_chat_members,
        )
    )

    dispatcher.add_handler(
        CommandHandler(
            command='sayhi',
            filters=Filters.group,
            callback=_group_command_welcome,
        )
    )


def _delete_notification_if_full_name_too_long(members, message: telegram.Message):
    for member in members:
        if len(member.full_name) > group_bot.FULL_NAME_TOO_LONG:
            message.delete()


def _send_welcome(update, context, members):
    path_to_file = os.path.join(os.path.join(be.BOT_DATA_DIR, 'resp'), 'welcome.md')

    if not os.path.exists(path_to_file):
        return

    with codecs.open(path_to_file, 'r', encoding='utf-8') as f:
        content = f.read().format(
            members=', '.join(members),
            project_name=kvs['project_name'],
            base_url=kvs['base_url'],
            key=kvs['key'],
            owner_name=kvs['owner_name'],
            rules=kvs['rules'],
        )

        paras = lf.list2solid(content.split('/-/'))

    i = 0
    for para in paras:
        if not para.startswith('///'):
            message = None

            if para.startswith('trigger!!!'):
                arr = lf.list2solid(para.split('!!!'))
                if len(arr) > 1:
                    if arr[1] == 'status':
                        send_status(update, context)

            elif para.startswith('forward!!!'):
                """ forward """
                arr = lf.list2solid(para.split('!!!')[1].split(','))
                if len(arr) > 1:
                    message = context.bot.forward_message(
                        chat_id=update.effective_chat.id,
                        from_chat_id=int(arr[0]),
                        message_id=int(arr[1]),
                    ).result()

            else:
                """ text message """
                message = context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=para,
                    disable_web_page_preview=True,
                ).result()

            i += 1
            if message:
                _previous(i, message, update, context)

                hf.para_sleep(para, i)


def _previous(i, message, update, context):
    if message:
        cache_previous_key = '{chat_id}_welcome{i}'.format(chat_id=update.effective_chat.id, i=i)

        previous_id = Cache.get(cache_previous_key)
        Cache.put(cache_previous_key, message.message_id)

        if previous_id:
            context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=previous_id,
            )


def _is_bot_joined(update, context):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            return True
    return False


@run_async
def _new_chat_members(update, context):
    """When new member(s) joined a group, send welcome text, and remove the previous"""

    if group_bot.REMOVE_FOOTPRINT:
        update.effective_message.delete()
    else:
        # delete notification message, if a full name is too long
        _delete_notification_if_full_name_too_long(update.message.new_chat_members, update.effective_message)

        # when bot joined
        if _is_bot_joined(update, context):
            send_status(update, context)
            return

        # send_status(update, context)

        # new members
        cache_members_key = '{chat_id}_welcome_members'.format(chat_id=update.effective_chat.id)
        members = Cache.get(cache_members_key, [])
        for member in update.message.new_chat_members:
            if len(member.full_name) <= group_bot.FULL_NAME_TOO_LONG and member.mention_markdown() not in members:
                members.append(member.mention_markdown())

        # cache timestamp
        timestamp_key = '{chat_id}_welcome_timestamp'.format(chat_id=update.effective_chat.id)
        prev_timestamp = Cache.get(timestamp_key, 0)
        curr_timestamp = time.time()

        if curr_timestamp - prev_timestamp < 120:
            Cache.put(cache_members_key, members)
            return
        else:
            Cache.put(timestamp_key, time.time())

        # forget: cache members
        Cache.forget(cache_members_key)

        # send welcome message(s)
        _send_welcome(update, context, members)


@run_async
def _group_command_welcome(update, context):
    # new members
    cache_members_key = '{chat_id}_welcome_members'.format(chat_id=update.effective_chat.id)
    members = Cache.get(cache_members_key, [])

    # cache timestamp
    timestamp_key = '{chat_id}_welcome_timestamp'.format(chat_id=update.effective_chat.id)
    Cache.put(timestamp_key, time.time())

    # forget: cache members
    Cache.forget(cache_members_key)

    # send welcome message(s)
    _send_welcome(update, context, members)
