import time
from telegram.ext import (Dispatcher, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async
from conf import env
from libs.GroupBotORM import *
from libs.group.kvs import kvs
from . import functions as hf

COMMAND = 'kick'


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        CommandHandler(
            command=COMMAND,
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

    if update.effective_message.reply_to_message.from_user.id == settings.BOT_ID:
        update.effective_message.delete()
        return

    # kick
    update.effective_chat.kick_member(
        user_id=update.effective_message.reply_to_message.from_user.id
    )

    # send tip message
    tip_message = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='`{full_name}`\n\n{preset}'.format(
            full_name=update.effective_message.reply_to_message.from_user.full_name,
            preset=kvs['group_command_kicked'],
        )
    ).result()

    # # sleep
    # time.sleep(env.SLEEP_SECONDS)
    #
    # # delete tip message
    # tip_message.delete()
