from libs.GroupBotORM import (db_bot, db_kv, db_qa, Chat, User, ChatAdmin, KeyValue, QATopic, QATag, QAAsk, QAReply)
from libs.CacheORM import (db_cache, Cache)


def main():
    print('main')


if __name__ == "__main__":
    with db_bot:
        db_bot.create_tables([Chat, User, ChatAdmin])

    with db_kv:
        db_kv.create_tables([KeyValue])

    with db_qa:
        db_qa.create_tables([QATopic, QATag, QAAsk, QAReply])

    with db_cache:
        db_cache.create_tables([Cache])

    main()
