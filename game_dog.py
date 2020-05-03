import libs.game as game
from libs import settings
from libs.FileCache import FileCache

# file cache
FC = FileCache(settings.DOG_DIR)


def main():
    cache_key = 'game_status'

    status = game.status()
    status['round_counter'] = 1
    status['timer'] = 1588481315

    FC.put(cache_key, status)

    print(status)


if __name__ == "__main__":
    main()
