import os
from libs import config_bot as config
from peewee import *
from playhouse.apsw_ext import APSWDatabase

import logging

# if be.DEBUG_MODE:
#     cleaner = logging.getLogger('peewee')
#     cleaner.addHandler(logging.StreamHandler())
#     cleaner.setLevel(logging.DEBUG)

db_bot = APSWDatabase(os.path.join(config.BOT_DATA_DIR, 'bot.db'))


class BotModel(Model):
    class Meta:
        database = db_bot


class Chat(BotModel):
    id = IntegerField(primary_key=True)
    type = CharField(max_length=16)
    title = CharField(null=True)
    can_send_messages = BooleanField()
    can_send_media_messages = BooleanField()
    can_send_polls = BooleanField()
    can_send_other_messages = BooleanField()
    can_add_web_page_previews = BooleanField()
    can_change_info = BooleanField()
    can_invite_users = BooleanField()
    can_pin_messages = BooleanField()

    def __str__(self):
        return '<Chat #{id} {title}>'.format(
            id=self.id,
            title=self.title,
        )


class User(BotModel):
    id = IntegerField(primary_key=True)
    is_bot = BooleanField()
    first_name = CharField(max_length=96, null=True)
    last_name = CharField(max_length=96, null=True)
    username = CharField(max_length=32, null=True)

    def __str__(self):
        return '<User #{id}>'.format(
            id=self.id,
        )


class ChatAdmin(BotModel):
    chat = ForeignKeyField(Chat, backref='admins')
    user = ForeignKeyField(User, backref='admin_chats')

    status = CharField(max_length=16)
    custom_title = CharField(max_length=16, null=True)
    until_date = DateTimeField(null=True)
    can_be_edited = BooleanField(null=True)

    can_change_info = BooleanField(null=True)
    can_post_messages = BooleanField(null=True)
    can_edit_messages = BooleanField(null=True)
    can_delete_messages = BooleanField(null=True)
    can_invite_users = BooleanField(null=True)
    can_restrict_members = BooleanField(null=True)
    can_pin_messages = BooleanField(null=True)
    can_promote_members = BooleanField(null=True)
    is_member = BooleanField(null=True)
    can_send_messages = BooleanField(null=True)
    can_send_media_messages = BooleanField(null=True)
    can_send_polls = BooleanField(null=True)
    can_send_other_messages = BooleanField(null=True)
    can_add_web_page_previews = BooleanField(null=True)

    def __str__(self):
        return '<ChatAdmin #{id}>'.format(
            id=self.id,
        )


db_kv = APSWDatabase(os.path.join(config.BOT_DATA_DIR, 'kvs.db'))


class ConfModel(Model):
    class Meta:
        database = db_kv


class KeyValue(ConfModel):
    key = CharField(max_length=32)
    value = TextField(null=True)


db_qa = APSWDatabase(os.path.join(config.BOT_DATA_DIR, 'qa.db'))


class QAModel(Model):
    class Meta:
        database = db_qa


class QATopic(QAModel):
    class Meta:
        table_name = 'topic'

    active = BooleanField(default=True)
    use_reply = BooleanField(default=False)
    show_title = BooleanField(default=False)
    title = CharField(max_length=64)
    remark = CharField(null=True)

    def __str__(self):
        return '<Topic #{id} {title}>'.format(
            id=self.id,
            title=self.title,
        )


class QATag(QAModel):
    class Meta:
        table_name = 'tag'

    topic = ForeignKeyField(QATopic, backref='tags')
    active = BooleanField(default=True)
    title = CharField(max_length=32)

    def __str__(self):
        return '<Tag #{id} #{title}>'.format(
            id=self.id,
            title=self.title,
        )

    def match(self, payload: str):
        if self.title == payload:
            return True

        if '#{}'.format(self.title) in payload:
            return True
        return False


class QAAsk(QAModel):
    class Meta:
        table_name = 'ask'

    MODE_STRICT = 0
    MODE_ORDER = 1
    MODE_DISORDER = 2

    topic = ForeignKeyField(QATopic, backref='asks')
    active = BooleanField(default=True)
    mode = SmallIntegerField(default=0)
    words = TextField(null=True)
    max = IntegerField(default=0, null=True)
    remark = CharField(null=True)

    def __str__(self):
        return '<Ask #{id} {mode}>'.format(
            id=self.id,
            mode=self.mode,
        )

    @staticmethod
    def _list(payload: list, els_to_remove: list = None):
        result = []

        for item in payload:
            if item not in result:
                result.append(item.strip())

        for el in els_to_remove or ['', None]:
            while el in result:
                result.remove(el)

        return result

    @property
    def list1(self):
        return self._list(str(self.words).replace('\n', '').replace('\r', '').strip(';').split(';'))

    @property
    def list2(self):
        list2 = []

        for line in self.list1:
            __clear = self._list(line.split(','))
            if __clear:
                list2.append(__clear)

        return list2

    @property
    def rows(self):
        rows = len(self.list1) + 1

        if rows > 2:
            return rows

        return 3

    def _mix(self, list2: list, i=1, target=None):
        # results with ';'
        __mixed = []

        if 1 > len(list2):
            return __mixed

        if 1 == len(list2):
            return list2[0]

        if target is None:
            target = list2[0]

        for s in target:
            for el in list2[i]:
                if not el.strip():
                    r = el
                else:
                    r = '%s;%s' % (s, el)

                if r not in __mixed:
                    __mixed.append(r)

        if i < len(list2) - 1:
            return self._mix(
                list2=list2,
                i=i + 1,
                target=__mixed,
            )

        # results without ';'
        results = []
        for row in __mixed:
            results.append(row.split(';'))

        return results

    def match(self, payload: str):
        if self.max and len(payload) > self.max:
            return None

        mixed_list = self._mix(self.list2)

        if self.MODE_STRICT == self.mode:
            for mixed in mixed_list:
                if ''.join(mixed) == payload:
                    return self

        elif self.MODE_ORDER == self.mode:
            for mixed in mixed_list:
                p = []
                for e in mixed:
                    p.append(payload.find(e))
                if -1 not in p and p == sorted(p):
                    return self

        elif self.MODE_DISORDER == self.mode:
            for mixed in mixed_list:

                __matched = True

                for el in mixed:
                    if el not in payload:
                        __matched = False

                if __matched is True:
                    return self

        return None


class QAReply(QAModel):
    class Meta:
        table_name = 'reply'

    topic = ForeignKeyField(QATopic, backref='replies')
    active = BooleanField(default=True)
    text = TextField(null=True)
    trigger = CharField(max_length=32, null=True)
    remark = CharField(null=True)

    def __str__(self):
        return '<Reply #{id}>'.format(
            id=self.id,
        )

    @property
    def lines(self):
        return str(self.text).split(';')
