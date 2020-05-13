import os
import peewee
import datetime
from libs import config_bot as config
from playhouse.apsw_ext import (APSWDatabase, DateTimeField)

db_logger = APSWDatabase(os.path.join(config.BOT_DATA_DIR, 'db_cleaner.db'))


class BaseModel(peewee.Model):
    class Meta:
        database = db_logger


class Chat(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    type = peewee.CharField(max_length=16)
    title = peewee.CharField(null=True)
    clean = peewee.BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    updated = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return '<Chat #{id} {title}>'.format(
            id=self.id,
            title=self.title,
        )

    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.now()
        return super(Chat, self).save(*args, **kwargs)


class User(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    first_name = peewee.CharField(max_length=32, null=True)
    last_name = peewee.CharField(max_length=32, null=True)
    created = DateTimeField(default=datetime.datetime.now)
    updated = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return '<User #{id} {first_name}>'.format(
            id=self.id,
            first_name=self.first_name,
        )

    @property
    def name(self):
        _names = list()
        if self.first_name:
            _names.append(str(self.first_name))
        if self.last_name:
            _names.append(str(self.last_name))

        return ' '.join(_names)

    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)


class ChatUser(BaseModel):
    chat = peewee.ForeignKeyField(Chat, backref='chat_users')
    user = peewee.ForeignKeyField(User, backref='chat_users')
    created = DateTimeField(default=datetime.datetime.now)
    updated = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return '<ChatUser #{id}>'.format(
            id=self.id,
        )

    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.now()
        return super(ChatUser, self).save(*args, **kwargs)
