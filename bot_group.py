from libs import shell
from libs import config_bot as config
from libs.MQBot import MQBot
from libs.group import handlers
from telegram.ext import Updater
from libs.GroupBotORM import (db_bot, db_kv, db_qa, Chat, User, ChatAdmin, KeyValue, QATopic, QATag, QAAsk, QAReply)
from libs.CacheORM import (db_cache, Cache)


def main():
    # bot
    bot = MQBot(token=config.BOT_TOKEN)

    # updater
    updater = Updater(
        bot=bot,
        use_context=True,
        request_kwargs=config.REQUEST_KWARGS,
    )

    # dispatcher
    dp = updater.dispatcher

    # private: `/start`
    handlers.private_command_start.attach(dp)

    # group: `/serve`
    handlers.group_command_serve.attach(dp)

    # group: commands
    handlers.group_command_kick.attach(dp)
    handlers.group_command_rules.attach(dp)
    handlers.group_command_game.attach(dp)
    handlers.group_command_resp.attach(dp)

    # group: new, left
    handlers.new_chat_members.attach(dp)
    handlers.left_chat_member.attach(dp)

    # group: text
    handlers.group_text.attach(dp)

    def start():
        updater.start_webhook(listen=config.SERVER_LISTEN,
                              port=config.BOT_PORT,
                              url_path=config.BOT_URL_PATH,
                              key=config.PATH_TO_KEY,
                              cert=config.PATH_TO_CERT,
                              webhook_url=config.BOT_WEBHOOK_URL)
        print('updater started.')
        return

    def stop():
        bot.stop_mq()
        updater.stop()
        print('updater stopped.')
        exit('Goodbye.')
        return

    start()

    if config.DEBUG_MODE:
        shell.embed()


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
