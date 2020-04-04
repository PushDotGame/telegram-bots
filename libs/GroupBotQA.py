from libs.GroupBotORM import *

asks = (Ask
        .select(Ask, Topic, Reply)
        .join(Topic, JOIN.LEFT_OUTER)
        .join(Reply, JOIN.LEFT_OUTER)
        .where((Ask.active == True) & (Topic.active == True) & (Reply.active == True))
        )
