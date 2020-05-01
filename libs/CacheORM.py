import os
import time
import json
import conf.bot as be
from peewee import *
from playhouse.apsw_ext import APSWDatabase
from . import functions as lf

import logging

# if be.DEBUG_MODE:
#     logger = logging.getLogger('peewee')
#     logger.addHandler(logging.StreamHandler())
#     logger.setLevel(logging.DEBUG)

db_cache = APSWDatabase(os.path.join(be.BOT_DATA_DIR, 'cache.db'))


class CacheModel(Model):
    class Meta:
        database = db_cache


class Cache(CacheModel):
    id = IntegerField(primary_key=True)
    hash = FixedCharField(32)
    value = TextField(null=True)
    expire = IntegerField(null=True)

    def __str__(self):
        return '<Cache #{id} {hash}>'.format(
            id=self.id,
            hash=self.hash,
        )


def put(key, value, expire: int = None):
    if expire:
        expire += time.time()

    value = json.dumps(value)

    cache, created = Cache.get_or_create(
        hash=lf.md5(key),
        defaults={
            'value': value,
            'expire': expire,
        }
    )

    if cache.value != value or cache.expire != expire:
        cache.value = value
        cache.expire = expire
        cache.save()

    return cache


def get(key, default=None):
    cache = Cache.get_or_none(hash=lf.md5(key))
    if cache:
        if cache.expire is None or cache.expire > time.time():
            return json.loads(cache.value)
        return default
    return default


def forget(key):
    q = Cache.delete().where(Cache.hash == lf.md5(key))
    q.execute()
    return True
