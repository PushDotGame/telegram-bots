from libs.GroupBotORM import *

asks = (Ask
        .select()
        .join(Topic)
        .join(Reply)
        .where((Ask.active == True) & (Topic.active == True) & (Reply.active == True))
        .prefetch(Topic, Reply)
        )

