import os
import time
import gettext
import libs.game as game
from libs import config
from libs.FileCache import FileCache
from libs import functions as lf

# file cache
FC = FileCache(config.DOG_DIR)


def main():
    # _ = (gettext
    #      .translation(os.path.splitext(__file__)[0], config.LOCALE_DIR, languages=[be.LANGUAGE, 'en-US'])
    #      .gettext
    #      )

    cache_key = 'game_status'

    status = FC.get(cache_key)

    print(status)

    # ss = list()
    #
    # ss.append(lf.text_kv(_('Block number:'), status['block_number']))
    # # ss.append(lf.kv_text('Round counter', status['round_counter']))
    # ss.append(lf.text_kv(_('Big-winners prize:'), '{} ETH'.format(status['winner_fund'])))
    # ss.append(lf.text_kv(_('Lucky-cookies prize:'), '{} ETH'.format(status['cookie_fund'])))

    # ss.append(lf.text_kv(_('Surprise issued:'), '{} ETH'.format(status['surprise_issued'])))
    # ss.append(lf.text_kv(_('Bonuses issued:'), '{} ETH'.format(status['bonus_issued'])))
    # ss.append(lf.text_kv(_('Lucky-cookies issued: {}:').format(status['cookie_counter']),
    #                      '{} ETH'.format(status['cookie_issued'])))
    # ss.append(lf.text_kv(_('Shareholders issued:'), '{} ETH'.format(status['shareholder_issued'])))
    #
    # print('\n'.join(ss))


if __name__ == "__main__":
    main()
