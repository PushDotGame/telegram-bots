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
        print('Not admin.')
        return

    print('Admin:')
    print(chat_admin)
    print('chat_admin.can_restrict_members:', chat_admin.can_restrict_members)


    #
    # if update.effective_user.id == env.BOT_OWNER_ID:
    #     print('is owner')
    #
    # # update.message.reply_text(
    # #     text=kvs['command_start'].format(
    # #         owner_name=kvs['owner_name'],
    # #         owner_username=kvs['owner_username'],
    # #     ),
    # #     reply_to_message_id=update.effective_message.message_id,
    # # )
