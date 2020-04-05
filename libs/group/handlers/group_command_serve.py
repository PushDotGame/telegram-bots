import telegram
from telegram.ext import (Dispatcher, CommandHandler, Filters)
from telegram.ext.dispatcher import run_async
from conf import env
from libs.GroupBotORM import *
from libs.group.kvs import kvs

COMMAND = 'serve'


def attach(dispatcher: Dispatcher):
    dispatcher.add_handler(
        CommandHandler(
            command=COMMAND,
            filters=Filters.group,
            callback=_group_command_serve,
        )
    )


def _permission_attr(key, chat_member: telegram.ChatMember, chat: telegram.Chat = None, is_creator: bool = False):
    if is_creator:
        return True

    value = getattr(chat_member, key)
    if value is not None:
        return value

    return getattr(chat, key, None)


@run_async
def _group_command_serve(update, context):
    if update.effective_user.id == env.BOT_OWNER_ID:
        message = update.message.reply_text(
            text=kvs['group_command_serve_updating'],
        ).result()

        try:
            effective_chat = context.bot.getChat(chat_id=update.effective_chat.id)

            # chat
            chat, created = Chat.get_or_create(
                id=effective_chat.id,
                defaults={
                    'type': effective_chat.type,
                    'title': effective_chat.title,
                    'can_send_messages': effective_chat.permissions.can_send_messages,
                    'can_send_media_messages': effective_chat.permissions.can_send_media_messages,
                    'can_send_polls': effective_chat.permissions.can_send_polls,
                    'can_send_other_messages': effective_chat.permissions.can_send_other_messages,
                    'can_add_web_page_previews': effective_chat.permissions.can_add_web_page_previews,
                    'can_change_info': effective_chat.permissions.can_change_info,
                    'can_invite_users': effective_chat.permissions.can_invite_users,
                    'can_pin_messages': effective_chat.permissions.can_pin_messages,
                }
            )

            if (chat.type != effective_chat.type
                    or chat.title != effective_chat.title
                    or chat.can_send_messages != effective_chat.permissions.can_send_messages
                    or chat.can_send_media_messages != effective_chat.permissions.can_send_media_messages
                    or chat.can_send_polls != effective_chat.permissions.can_send_polls
                    or chat.can_send_other_messages != effective_chat.permissions.can_send_other_messages
                    or chat.can_add_web_page_previews != effective_chat.permissions.can_add_web_page_previews
                    or chat.can_change_info != effective_chat.permissions.can_change_info
                    or chat.can_invite_users != effective_chat.permissions.can_invite_users
                    or chat.can_pin_messages != effective_chat.permissions.can_pin_messages):
                chat.type = effective_chat.type
                chat.title = effective_chat.title
                chat.can_send_messages = effective_chat.permissions.can_send_messages
                chat.can_send_media_messages = effective_chat.permissions.can_send_media_messages
                chat.can_send_polls = effective_chat.permissions.can_send_polls
                chat.can_send_other_messages = effective_chat.permissions.can_send_other_messages
                chat.can_add_web_page_previews = effective_chat.permissions.can_add_web_page_previews
                chat.can_change_info = effective_chat.permissions.can_change_info
                chat.can_invite_users = effective_chat.permissions.can_invite_users
                chat.can_pin_messages = effective_chat.permissions.can_pin_messages
                chat.save()

            # admins
            for admin in effective_chat.get_administrators():
                is_creator = admin.status == telegram.ChatMember.CREATOR
                print('admin:', admin)

                # user
                user, created = User.get_or_create(
                    id=admin.user.id,
                    defaults={
                        'is_bot': admin.user.is_bot,
                        'first_name': admin.user.first_name,
                        'last_name': admin.user.last_name,
                        'username': admin.user.username,
                    }
                )

                if (user.first_name != admin.user.first_name
                        or user.last_name != admin.user.last_name
                        or user.username != admin.user.username):
                    user.first_name = admin.user.first_name
                    user.last_name = admin.user.last_name
                    user.username = admin.user.username
                    user.save()

                # chat_admin
                chat_admin, created = ChatAdmin.get_or_create(
                    chat=chat,
                    user=user,
                    defaults={
                        'status': admin.status,
                        'custom_title': admin.custom_title,
                        'until_date': admin.until_date,
                        'can_be_edited': admin.can_be_edited,
                        'can_change_info': _permission_attr('can_change_info',
                                                            admin, chat, is_creator),
                        'can_post_messages': _permission_attr('can_post_messages',
                                                              admin, chat, is_creator),
                        'can_edit_messages': admin.can_edit_messages,
                        'can_delete_messages': _permission_attr('can_delete_messages',
                                                                admin, chat, is_creator),
                        'can_invite_users': _permission_attr('can_invite_users',
                                                             admin, chat, is_creator),
                        'can_restrict_members': _permission_attr('can_restrict_members',
                                                                 admin, chat, is_creator),
                        'can_pin_messages': _permission_attr('can_pin_messages',
                                                             admin, chat, is_creator),
                        'can_promote_members': _permission_attr('can_promote_members',
                                                                admin, chat, is_creator),
                        'is_member': admin.is_member,
                        'can_send_messages': _permission_attr('can_send_messages',
                                                              admin, chat, is_creator),
                        'can_send_media_messages': _permission_attr('can_send_media_messages',
                                                                    admin, chat, is_creator),
                        'can_send_polls': _permission_attr('can_send_polls',
                                                           admin, chat, is_creator),
                        'can_send_other_messages': _permission_attr('can_send_other_messages',
                                                                    admin, chat, is_creator),
                        'can_add_web_page_previews': _permission_attr('can_add_web_page_previews',
                                                                      admin, chat, is_creator),
                    }
                )

                if (chat_admin.status != admin.status
                        or chat_admin.custom_title != admin.custom_title
                        or chat_admin.until_date != admin.until_date
                        or chat_admin.can_be_edited != admin.can_be_edited
                        or chat_admin.can_change_info != _permission_attr('can_change_info',
                                                                          admin, chat, is_creator)
                        or chat_admin.can_post_messages != admin.can_post_messages
                        or chat_admin.can_edit_messages != admin.can_edit_messages
                        or chat_admin.can_delete_messages != _permission_attr('can_delete_messages',
                                                                              admin, chat, is_creator)
                        or chat_admin.can_invite_users != _permission_attr('can_invite_users',
                                                                           admin, chat, is_creator)
                        or chat_admin.can_restrict_members != _permission_attr('can_restrict_members',
                                                                               admin, chat, is_creator)
                        or chat_admin.can_pin_messages != _permission_attr('can_pin_messages',
                                                                           admin, chat, is_creator)
                        or chat_admin.can_promote_members != _permission_attr('can_promote_members',
                                                                              admin, chat, is_creator)
                        or chat_admin.is_member != admin.is_member
                        or chat_admin.can_send_messages != _permission_attr('can_send_messages',
                                                                            admin, chat, is_creator)
                        or chat_admin.can_send_media_messages != _permission_attr('can_send_media_messages',
                                                                                  admin, chat, is_creator)
                        or chat_admin.can_send_polls != _permission_attr('can_send_polls',
                                                                         admin, chat, is_creator)
                        or chat_admin.can_send_other_messages != _permission_attr('can_send_other_messages',
                                                                                  admin, chat, is_creator)
                        or chat_admin.can_add_web_page_previews != _permission_attr('can_add_web_page_previews',
                                                                                    admin, chat, is_creator)):
                    chat_admin.status = admin.status
                    chat_admin.custom_title = admin.custom_title
                    chat_admin.until_date = admin.until_date
                    chat_admin.can_be_edited = admin.can_be_edited
                    chat_admin.can_change_info = _permission_attr('can_change_info',
                                                                  admin, chat, is_creator)
                    chat_admin.can_post_messages = admin.can_post_messages
                    chat_admin.can_edit_messages = admin.can_edit_messages
                    chat_admin.can_delete_messages = _permission_attr('can_delete_messages',
                                                                      admin, chat, is_creator)
                    chat_admin.can_invite_users = _permission_attr('can_invite_users',
                                                                   admin, chat, is_creator)
                    chat_admin.can_restrict_members = _permission_attr('can_restrict_members',
                                                                       admin, chat, is_creator)
                    chat_admin.can_pin_messages = _permission_attr('can_pin_messages',
                                                                   admin, chat, is_creator)
                    chat_admin.can_promote_members = _permission_attr('can_promote_members',
                                                                      admin, chat, is_creator)
                    chat_admin.is_member = admin.is_member
                    chat_admin.can_send_messages = _permission_attr('can_send_messages',
                                                                    admin, chat, is_creator)
                    chat_admin.can_send_media_messages = _permission_attr('can_send_media_messages',
                                                                          admin, chat, is_creator)
                    chat_admin.can_send_polls = _permission_attr('can_send_polls',
                                                                 admin, chat, is_creator)
                    chat_admin.can_send_other_messages = _permission_attr('can_send_other_messages',
                                                                          admin, chat, is_creator)
                    chat_admin.can_add_web_page_previews = _permission_attr('can_add_web_page_previews',
                                                                            admin, chat, is_creator)
                    chat_admin.save()

            message.edit_text(
                text='{}\n\n{}'.format(kvs['group_command_serve_updating'], kvs['group_command_serve_finished'])
            )

        except Exception as e:
            message.edit_text(
                text='{}\n\n*Exception:*\n`{}`'.format(kvs['group_command_serve_updating'], e)
            )


"""
Overwrite if none:

    can_send_messages
    can_send_media_messages
    can_send_polls
    can_send_other_messages
    can_add_web_page_previews
    can_change_info
    can_invite_users
    can_pin_messages
"""
