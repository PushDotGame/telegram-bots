from libs.GroupBotORM import *


def get_admin_chat(update):
    query = (ChatAdmin
             .select()
             .join(Chat)
             .switch(ChatAdmin)
             .join(User)
             .where((Chat.id == update.effective_chat.id) & (User.id == update.effective_user.id))
             )

    if query:
        return query[0]
    else:
        return None

