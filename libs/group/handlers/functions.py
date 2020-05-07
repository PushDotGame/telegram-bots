import time
import random
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


def para_sleep(para, i: int):
    if i % 2 > 0:
        time.sleep(max(3, min(10, int(len(para) / 19))))
    else:
        time.sleep(random.randint(10, 15))
