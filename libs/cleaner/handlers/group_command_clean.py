import telegram
from telegram.ext import (Dispatcher, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.CleanerORM import Chat
from libs import config_bot as config


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        CommandHandler(
            command='clean',
            filters=Filters.group,
            callback=_group_command_clean,
        )
    )


@run_async
def _group_command_clean(update, context):
    if update.effective_user.id == config.BOT_OWNER_ID:
        message = update.message.reply_text('*Setting...*').result()

        clean = True

        try:
            if len(context.args) > 0 and str(context.args[0]).strip().lower() in ['0', 'off', 'false']:
                clean = False

            # chat
            cleaner_chat, created = Chat.get_or_create(
                id=update.effective_chat.id,
                defaults={
                    'type': update.effective_chat.type,
                    'title': update.effective_chat.title,
                    'clean': clean
                }
            )

            if (cleaner_chat.type != update.effective_chat.type
                    or cleaner_chat.title != update.effective_chat.title
                    or cleaner_chat.clean != clean):
                cleaner_chat.type = update.effective_chat.type
                cleaner_chat.title = update.effective_chat.title
                cleaner_chat.clean = clean
                cleaner_chat.save()

            if clean:
                message.edit_text('`CLEAN_MODE`\n\n*Turned ON*')
            else:
                message.edit_text('`CLEAN_MODE`\n\n*Turned OFF*')

        except Exception as e:
            message.edit_text(
                text='*Exception:*\n`{}`'.format(e)
            )
