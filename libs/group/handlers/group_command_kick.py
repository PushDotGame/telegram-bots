from telegram.ext import (Dispatcher, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.group.kvs import kvs
from . import functions as hf
from libs import config_bot as config
from libs import CacheORM as Cache


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        CommandHandler(
            command='out',
            filters=Filters.group,
            callback=_group_command_kick,
        )
    )


@run_async
def _group_command_kick(update, context):
    chat_admin = hf.get_admin_chat(update)
    if chat_admin is None:
        return

    if not chat_admin.can_restrict_members:
        return

    if update.effective_message.reply_to_message is None:
        return

    if update.effective_message.reply_to_message.from_user.id == config.BOT_ID:
        update.effective_message.delete()
        return

    # cache user id
    key = '{chat_id}_kick_user_id'.format(chat_id=update.effective_chat.id)
    Cache.put(key, update.effective_message.reply_to_message.from_user.id)

    # kick
    update.effective_chat.kick_member(
        user_id=update.effective_message.reply_to_message.from_user.id
    ).result()

    # send tip message
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='_{full_name}_\n\n{preset}'.format(
            full_name=update.effective_message.reply_to_message.from_user.full_name,
            preset=kvs['group_command_kicked'],
        )
    ).result()
