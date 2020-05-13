from telegram.ext import (Dispatcher, MessageHandler, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.CleanerORM import (Chat, User, ChatUser)


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        MessageHandler(
            filters=Filters.status_update.new_chat_members,
            callback=_new_chat_members,
        )
    )


@run_async
def _new_chat_members(update, context):
    cleaner_chat, created = Chat.get_or_create(
        id=update.effective_chat.id,
        defaults={
            'type': update.effective_chat.type,
            'title': update.effective_chat.title,
        }
    )

    if cleaner_chat.clean:
        update.effective_message.delete()

    for member in update.message.new_chat_members:
        cleaner_user, created = User.get_or_create(id=member.id,
                                                  defaults={
                                                      'first_name': member.first_name,
                                                      'last_name': member.last_name
                                                  })

        if (cleaner_user.first_name != member.first_name
                or cleaner_user.last_name != member.last_name):
            cleaner_user.first_name = member.first_name
            cleaner_user.last_name = member.last_name
            cleaner_user.save()

        ChatUser.get_or_create(chat=cleaner_chat, user=cleaner_user)
