import os
from libs import config
from decimal import Decimal
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(
    endpoint_uri=config.WEB3_HTTP_PROVIDER,
))

with open(os.path.join(config.CONTRACTS_DIR, 'game.json'), 'r') as f:
    game_abi = f.read().strip()

GAME_CONTRACT = w3.eth.contract(
    abi=game_abi,
    address=w3.toChecksumAddress(config.GAME_ADDRESS),
)


def block_number():
    return w3.eth.blockNumber


def status():
    payload = GAME_CONTRACT.functions.getStatus().call()
    return {
        'block_number': block_number(),
        'timer': payload[0],
        'round_counter': payload[1],
        'player_counter': payload[2],
        'message_counter': payload[3],
        'cookie_counter': payload[4],

        'cookie_fund': Decimal(w3.fromWei(payload[5], 'ether')),
        'winner_fund': Decimal(w3.fromWei(payload[6], 'ether')),

        'surprise_issued': Decimal(w3.fromWei(payload[7], 'ether')),
        'bonus_issued': Decimal(w3.fromWei(payload[8], 'ether')),
        'cookie_issued': Decimal(w3.fromWei(payload[9], 'ether')),
        'shareholder_issued': Decimal(w3.fromWei(payload[10], 'ether')),
    }
