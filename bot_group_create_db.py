from libs.GroupBotORM import *
from libs.CacheORM import *


def main():
    with db_bot:
        db_bot.create_tables([Chat, User, ChatAdmin])

    with db_kv:
        db_kv.create_tables([KeyValue])

    with db_qa:
        db_qa.create_tables([Topic, Ask, Reply])

    with db_cache:
        db_cache.create_tables([Cache])


if __name__ == "__main__":
    main()
