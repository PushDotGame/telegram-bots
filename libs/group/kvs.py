from ..GroupBotORM import *

kvs = {
    'owner_name': 'your-name',
    'owner_username': 'your-username',

    'command_start': "Here is {owner_name}'s bot."
                     "\n\nContact @{owner_username} if you need."
                     "\n\n`No one can see the message you sent here`",

    'welcome': 'Welcome {members}'
               '\n\n{rules}',

    'rules': 'rules-text',

    'group_command_serve_updating': '`Updating ..`',
    'group_command_serve_finished': '*Update accomplished.*',

    'group_command_kicked': 'Have already been removed from this group.'
}

rows = KeyValue.select()

for row in rows:
    kvs[row.key] = row.value.replace('\r\n', '\n')
