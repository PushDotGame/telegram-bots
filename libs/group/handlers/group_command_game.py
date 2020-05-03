import os
import time
import random
import gettext
from telegram.ext import (Dispatcher, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async
from libs.group.kvs import kvs
from . import functions as hf
from conf import bot as be
from libs import CacheORM as Cache
from libs.FileCache import FileCache
from libs import settings
from libs import functions as lf

# file cache
FC = FileCache(settings.DOG_DIR)


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        CommandHandler(
            command='game',
            filters=Filters.group,
            callback=_group_command_game,
        )
    )


@run_async
def _group_command_game(update, context):
    _ = gettext.translation(domain=os.path.splitext(os.path.basename(__file__))[0],
                            localedir=settings.LOCALE_DIR,
                            languages=[be.LANGUAGE],
                            fallback=True,
                            ).gettext

    cache_key = 'game_status'

    status = FC.get(cache_key)
    if status:
        print(status)

        # prize & countdown
        text_prize = list()
        text_prize.append(lf.text_kv(_('Block number'), status['block_number']))

        if status['round_counter'] > 0:
            text_prize.append(_('\n*Round #{}*\n').format(status['round_counter']))

        text_prize.append(lf.text_kv(_('Big-winners PRIZE'), '{} ETH'.format(status['winner_fund'])))
        text_prize.append(lf.text_kv(_('Lucky-cookies PRIZE'), '{} ETH'.format(status['cookie_fund'])))

        if status['round_counter'] < 1:
            text_prize.append(_('\nGame has not started yet.'))
        else:
            seconds = int(status['timer'] - time.time())
            if seconds > 0:
                text_prize.append(lf.text_kv(_('Countdown'), lf.seconds2countdown(seconds)))
            else:
                text_prize.append(_('\n*Countdown ENDED*'))

        update.message.reply_text('\n'.join(text_prize))

        # bonus
        if status['round_counter'] > 0:
            text_bonus = list()
            text_bonus.append(_('*Total bonus*\n'))
            if status['surprise_issued'] > 0:
                text_bonus.append(lf.text_kv(_('Surprise'), '{} ETH'.format(status['surprise_issued'])))
            if status['bonus_issued'] > 0:
                text_bonus.append(lf.text_kv(_('Bonuses'), '{} ETH'.format(status['bonus_issued'])))
            if status['cookie_counter'] > 0:
                text_bonus.append(lf.text_kv(_('{} lucky-cookies').format(status['cookie_counter']),
                                             '{} ETH'.format(status['cookie_issued'])))
            if status['shareholder_issued'] > 0:
                text_bonus.append(lf.text_kv(_('Shareholders'), '{} ETH'.format(status['shareholder_issued'])))

            time.sleep(random.randint(1, 3))
            update.message.reply_text('\n'.join(text_bonus))

    # chat_admin = hf.get_admin_chat(update)
    # if chat_admin is None:
    #     return
    #
    # if not chat_admin.can_restrict_members:
    #     return
    #
    # if update.effective_message.reply_to_message is None:
    #     return
    #
    # if update.effective_message.reply_to_message.from_user.id == be.BOT_ID:
    #     update.effective_message.delete()
    #     return
    #
    # # cache user id
    # key = '{chat_id}_kick_user_id'.format(chat_id=update.effective_chat.id)
    # Cache.put(key, update.effective_message.reply_to_message.from_user.id)
    #
    # # kick
    # update.effective_chat.kick_member(
    #     user_id=update.effective_message.reply_to_message.from_user.id
    # ).result()
    #
    # # send tip message
    # context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text='_{full_name}_\n\n{preset}'.format(
    #         full_name=update.effective_message.reply_to_message.from_user.full_name,
    #         preset=kvs['group_command_kicked'],
    #     )
    # ).result()
