import libs.game as game
from libs import settings
from libs.FileCache import FileCache

# file cache
FC = FileCache(settings.DOG_DIR)


def main():
    cache_key = 'game_status'

    status = FC.get(cache_key)

    print(status)


if __name__ == "__main__":
    main()
