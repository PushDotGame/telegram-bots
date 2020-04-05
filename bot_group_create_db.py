from libs.GroupBotORM import *


def main():
    with db_bot:
        db_bot.create_tables([Chat, User, ChatAdmin])

    with db_kv:
        db_kv.create_tables([KeyValue])

    with db_qa:
        db_qa.create_tables([Topic, Ask, Reply])


if __name__ == "__main__":
    main()
