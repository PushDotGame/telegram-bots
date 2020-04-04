from libs.GroupBotORM import *
import logging

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def main():
    with qa:
        qa.create_tables([Topic, Ask, Reply])


if __name__ == "__main__":
    main()
