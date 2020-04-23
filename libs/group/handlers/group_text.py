import time
import random
from telegram.ext import (Dispatcher, MessageHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.group.kvs import kvs
from libs.group.qa import asks
import libs.functions as lf


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        MessageHandler(
            filters=Filters.group & Filters.text,
            callback=_group_text,
        )
    )


@run_async
def _group_text(update, context):
    message_text = update.effective_message.text.strip().lower()

    for ask in asks:
        if ask.match(message_text):
            topic = ask.topic
            replies = list()

            for reply in topic.replies:
                if reply.active:
                    replies.append(reply)

            reply = replies[random.randint(0, len(replies) - 1)]

            # if reply.trigger:
            #     """trigger"""
            #
            #     update.message.reply_text(
            #         text='trigger: {}'.format(reply.trigger),
            #     )
            #
            # else:
            #     """text"""

            # show title
            if topic.show_title:
                text = '`《{title}》`' \
                       '\n\n{content}'.format(title=topic.title,
                                              content='\n\n'.join(reply.lines),
                                              )
            else:
                text = '\n\n'.join(reply.lines)

            text = text.format(
                base_url=kvs['base_url'],
                key=kvs['key'],
                owner_name=kvs['owner_name']
            )

            text_messages = lf.list2solid(text.split('/-/'))

            i = 0
            for text_message in text_messages:
                if ask.topic.use_reply and i == 0:
                    """use reply"""
                    update.message.reply_text(
                        text=text_message,
                        disable_web_page_preview=True,
                    )

                else:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=text_message,
                        disable_web_page_preview=True,
                    )

                time.sleep(max(random.randint(1, 3), min(4, int(len(text_message) / 35))))
                i += 1

            break
