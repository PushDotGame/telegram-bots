import os
import time
import random
import gettext
from conf import bot as be
from libs.FileCache import FileCache
from libs import settings
from libs import functions as lf

# file cache
FC = FileCache(settings.DOG_DIR)


def send_status(update, context, reply: bool = False, part2: bool = False):
    _ = gettext.translation(domain=os.path.splitext(os.path.basename(__file__))[0],
                            localedir=settings.LOCALE_DIR,
                            languages=[be.LANGUAGE],
                            fallback=True,
                            ).gettext

    cache_key = 'game_status'

    status = FC.get(cache_key)
    if status:

        # prize & countdown
        text_prize = list()
        text_prize.append(lf.text_kv(_('ETH block number'), status['block_number']))

        if status['round_counter'] > 0:
            text_prize.append('\n' + lf.text_title(_('Game: Round #{}').format(status['round_counter'])) + '\n')
        else:
            text_prize.append('\n' + lf.text_title(_('Current STATUS')) + '\n')

        text_prize.append(lf.text_kv(_('Big-winners PRIZE'), '{} ETH'.format(status['winner_fund'])))
        text_prize.append(lf.text_kv(_('Lucky-cookies PRIZE'), '{} ETH'.format(status['cookie_fund'])))

        if status['round_counter'] < 1:
            text_prize.append('\n'
                              + _('Round #{round_counter} will start after a PUSH')
                              .format(round_counter=status['round_counter'] + 1)
                              )
        else:
            seconds = int(status['timer'] - time.time())
            if seconds > 0:
                text_prize.append(lf.text_kv(_('Countdown'), lf.seconds2countdown(seconds)))
            else:
                text_prize.append('\n*' + _('Countdown ENDED') + '*')
                text_prize.append('*'
                                  + _('Round #{round_counter} will start after next PUSH')
                                  .format(round_counter=status['round_counter'] + 1)
                                  + '*'
                                  )

        if reply:
            update.message.reply_text('\n'.join(text_prize))
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='\n'.join(text_prize),
            )

        # part2
        if part2:

            # bonus
            if status['round_counter'] > 0:

                text_bonus = list()
                text_bonus.append(lf.text_title(_('Total bonus issued')) + '\n')

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

                if reply:
                    update.message.reply_text('\n'.join(text_bonus))
                else:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text='\n'.join(text_bonus),
                    )
