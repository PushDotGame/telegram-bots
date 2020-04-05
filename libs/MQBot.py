from telegram import ParseMode
from telegram.bot import Bot
from telegram.ext import messagequeue as mq


class MQBot(Bot):
    """
    A subclass of Bot which delegates send method handling to MQ
    """

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)

        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue(
            all_burst_limit=29,
            all_time_limit_ms=1017,
            group_burst_limit=19,
            group_time_limit_ms=60000,
        )
        self._parse_mode = ParseMode.MARKDOWN

    def __del__(self):
        self.stop_mq()

    def stop_mq(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super(MQBot, self).send_message(
            parse_mode=self._parse_mode,
            *args,
            **kwargs
        )

    @mq.queuedmessage
    def edit_message_text(self, *args, **kwargs):
        return super(MQBot, self).edit_message_text(
            parse_mode=self._parse_mode,
            *args,
            **kwargs
        )

    @mq.queuedmessage
    def delete_message(self, *args, **kwargs):
        return super(MQBot, self).delete_message(
            *args, **kwargs
        )

    @mq.queuedmessage
    def forward_message(self, *args, **kwargs):
        return super(MQBot, self).forward_message(
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_photo(self, *args, **kwargs):
        return super(MQBot, self).send_photo(
            parse_mode=self._parse_mode,
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_audio(self, *args, **kwargs):
        return super(MQBot, self).send_audio(
            parse_mode=self._parse_mode,
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_document(self, *args, **kwargs):
        return super(MQBot, self).send_document(
            parse_mode=self._parse_mode,
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_sticker(self, *args, **kwargs):
        return super(MQBot, self).send_sticker(
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_video(self, *args, **kwargs):
        return super(MQBot, self).send_video(
            parse_mode=self._parse_mode,
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_video_note(self, *args, **kwargs):
        return super(MQBot, self).send_video_note(
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_animation(self, *args, **kwargs):
        return super(MQBot, self).send_animation(
            parse_mode=self._parse_mode,
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_voice(self, *args, **kwargs):
        return super(MQBot, self).send_voice(
            parse_mode=self._parse_mode,
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_media_group(self, *args, **kwargs):
        return super(MQBot, self).send_media_group(
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_location(self, *args, **kwargs):
        return super(MQBot, self).send_location(
            *args, **kwargs
        )

    @mq.queuedmessage
    def edit_message_live_location(self, *args, **kwargs):
        return super(MQBot, self).edit_message_live_location(
            *args, **kwargs
        )

    @mq.queuedmessage
    def stop_message_live_location(self, *args, **kwargs):
        return super(MQBot, self).stop_message_live_location(
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_venue(self, *args, **kwargs):
        return super(MQBot, self).send_venue(
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_contact(self, *args, **kwargs):
        return super(MQBot, self).send_contact(
            *args, **kwargs
        )

    @mq.queuedmessage
    def send_game(self, *args, **kwargs):
        return super(MQBot, self).send_game(
            *args, **kwargs
        )
