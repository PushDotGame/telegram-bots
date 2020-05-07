from libs.GroupBotORM import *

tags = (QATag
        .select()
        .join(QATopic)
        .join(QAReply)
        .where((QATag.active == True) & (QATopic.active == True) & (QAReply.active == True))
        .prefetch(QATopic, QAReply)
        )

asks = (QAAsk
        .select()
        .join(QATopic)
        .join(QAReply)
        .where((QAAsk.active == True) & (QATopic.active == True) & (QAReply.active == True))
        .prefetch(QATopic, QAReply)
        )
