import telegram
import time
import random
from telegram.ext import (Dispatcher, MessageHandler, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.group.kvs import kvs
from conf import group_bot
from conf import bot as be
from libs.FileCache import FileCache

# file cache
FC = FileCache(be.BOT_CACHE_DIR)


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        MessageHandler(
            filters=Filters.status_update.new_chat_members,
            callback=_new_chat_members,
        )
    )

    dispatcher.add_handler(
        CommandHandler(
            command='welcome',
            filters=Filters.group,
            callback=_group_command_welcome,
        )
    )


def _delete_notification_if_full_name_too_long(members, message: telegram.Message):
    for member in members:
        if len(member.full_name) > group_bot.FULL_NAME_TOO_LONG:
            message.delete()


@run_async
def _new_chat_members(update, context):
    """When new member(s) joined a group, send welcome text, and remove the previous"""

    if group_bot.REMOVE_FOOTPRINT:
        update.effective_message.delete()
    else:
        # delete notification message, if a full name is too long
        _delete_notification_if_full_name_too_long(update.message.new_chat_members, update.effective_message)

        # # when bot joined
        # for member in update.message.new_chat_members:
        #     if member.id == context.bot.id:
        #         update.message.reply_text(text='Hi')
        #         break

        # new members
        cache_members_key = '{chat_id}_welcome_members'.format(chat_id=update.effective_chat.id)
        members = FC.get(cache_members_key, [])
        for member in update.message.new_chat_members:
            if len(member.full_name) <= group_bot.FULL_NAME_TOO_LONG and member.mention_markdown() not in members:
                members.append(member.mention_markdown())

        # cache timestamp
        timestamp_key = '{chat_id}_welcome_timestamp'.format(chat_id=update.effective_chat.id)
        prev_timestamp = FC.get(timestamp_key, 0)
        curr_timestamp = time.time()

        if curr_timestamp - prev_timestamp < 120:
            FC.put(cache_members_key, members)
            return
        else:
            FC.put(timestamp_key, time.time())

        # forget: cache members
        FC.forget(cache_members_key)

        # send welcome
        message = context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=kvs['welcome'].format(
                members=', '.join(members),
                base_url=kvs['base_url'],
                rules=kvs['rules'],
            ),
            disable_web_page_preview=True,
        ).result()

        # cache, then delete the previous
        if message:
            try:
                key = '{chat_id}_welcome'.format(chat_id=update.effective_chat.id)

                previous_id = FC.get(key)
                FC.put(key, message.message_id)

                if previous_id:
                    context.bot.delete_message(
                        chat_id=update.effective_chat.id,
                        message_id=previous_id,
                    )
            except Exception as e:
                print(e)

        # welcome 1
        if 'welcome1' in kvs:
            time.sleep(random.randint(5, 10))

            # send welcome
            message1 = context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=kvs['welcome1'].format(
                    members=', '.join(members),
                    base_url=kvs['base_url'],
                    rules=kvs['rules'],
                ),
                disable_web_page_preview=True,
            ).result()

            # cache, then delete the previous
            if message1:
                try:
                    key1 = '{chat_id}_welcome1'.format(chat_id=update.effective_chat.id)

                    previous_id = FC.get(key1)
                    FC.put(key1, message1.message_id)

                    if previous_id:
                        context.bot.delete_message(
                            chat_id=update.effective_chat.id,
                            message_id=previous_id,
                        )
                except Exception as e:
                    print(e)


@run_async
def _group_command_welcome(update, context):
    # new members
    cache_members_key = '{chat_id}_welcome_members'.format(chat_id=update.effective_chat.id)
    members = FC.get(cache_members_key, [])

    # cache timestamp
    timestamp_key = '{chat_id}_welcome_timestamp'.format(chat_id=update.effective_chat.id)
    FC.put(timestamp_key, time.time())

    # forget: cache members
    FC.forget(cache_members_key)

    # send welcome
    message = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=kvs['welcome'].format(
            members=', '.join(members),
            base_url=kvs['base_url'],
            rules=kvs['rules'],
        ),
        disable_web_page_preview=True,
    ).result()

    # cache, then delete the previous
    if message:
        try:
            key = '{chat_id}_welcome'.format(chat_id=update.effective_chat.id)

            previous_id = FC.get(key)
            FC.put(key, message.message_id)

            if previous_id:
                context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=previous_id,
                )
        except Exception as e:
            print(e)

    # welcome 1
    if 'welcome1' in kvs:
        time.sleep(random.randint(5, 10))

        # send welcome
        message1 = context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=kvs['welcome1'].format(
                members=', '.join(members),
                base_url=kvs['base_url'],
                rules=kvs['rules'],
            ),
            disable_web_page_preview=True,
        ).result()

        # cache, then delete the previous
        if message1:
            try:
                key1 = '{chat_id}_welcome1'.format(chat_id=update.effective_chat.id)

                previous_id = FC.get(key1)
                FC.put(key1, message1.message_id)

                if previous_id:
                    context.bot.delete_message(
                        chat_id=update.effective_chat.id,
                        message_id=previous_id,
                    )
            except Exception as e:
                print(e)
