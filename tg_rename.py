import conf.pyrogram as pe
from pyrogram import Client
from pyrogram.api import functions
from libs.FileCache import FileCache

# file cache
FC = FileCache(pe.DOG_DIR)

# pyrogram
_app = Client(
    session_name=pe.SESSION_NAME,
    api_id=pe.PYROGRAM_API_ID,
    api_hash=pe.PYROGRAM_API_HASH,
    app_version=pe.PYROGRAM_APP_VERSION,
    device_model=pe.PYROGRAM_DEVICE_MODEL,
    system_version=pe.PYROGRAM_SYSTEM_VERSION,
    proxy=pe.PROXY,
    workdir=pe.TG_DATA_DIR,
    no_updates=True,
)


def rename(last_name: str):
    with _app as app:
        print('Last name: {}'.format(last_name))

        app.send(functions.account.UpdateProfile(
            last_name=last_name
        ))

        print('Renamed..')


def main():
    # cached status
    status = status = FC.get('game_status')

    if status is None:
        exit('Please run `python3 fetch.py` first')

    # status
    if status:
        round_counter = status['round_counter']
        fund = status['cookie_fund'] + status['winner_fund']

        # block_number = status['block_number']
        # timer = status['timer']
        # issued = status['surprise_issued'] \
        #          + status['bonus_issued'] \
        #          + status['cookie_issued'] \
        #          + status['shareholder_issued']

        # rename
        rename(last_name='🚀🚀 {} ETH++ 新游启动 点击来撩'.format(
            fund.quantize(pe.DECIMAL),
        ))


if __name__ == "__main__":
    main()
