import random
from telegram.ext import (Dispatcher, MessageHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.group.kvs import kvs
from libs.group.qa import asks


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
            replies = topic.replies

            reply = replies[random.randint(0, len(replies) - 1)]

            if reply.trigger:
                """trigger"""

                update.message.reply_text(
                    text='trigger: {}'.format(reply.trigger),
                )

            else:
                """text"""

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
                    owner_name=kvs['owner_name']
                )

                # use reply
                if ask.topic.use_reply:
                    update.message.reply_text(
                        text=text.format(),
                        disable_web_page_preview=True,
                    )
                else:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=text,
                        disable_web_page_preview=True,
                    )

            break
