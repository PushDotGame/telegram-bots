# Telegram forward/id bot

Tons of thanks to [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

## Bots


### Group BOT 群组辅助机器人

Auto match and reply, alpha now.

- Say hello
- Remove leaving footprint
- Match words and reply
- `/out` for kick



### Forward bot 自动转发机器人

Auto forward every private message to a specific group or channel.

自动转发每一条私聊消息到一个特定的群组或频道


### Answer id bot 应答 ID 机器人

Example: [@answer_id_bot](https://t.me/answer_id_bot)

Answer the group/channel/user id, when you need.

当你需要时，给出群组/频道/用户的 ID


If the above [@answer_id_bot](https://t.me/answer_id_bot) works well,
you may just need to use it once,
for getting a group/channel id.

如果上边的 [@answer_id_bot](https://t.me/answer_id_bot)
工作良好，你也许只需要它一次，用于取得群组或频道的 ID




## A brief guide for deploy

### Ubuntu 18.04 LTS

...


### pip3

```console
$ sudo apt python3-dev
$ wget https://bootstrap.pypa.io/get-pip.py
$ python3 get-pip.py
```


### python-dotenv, python-telegram-bot

```console
$ pip3 install -U python-dotenv python-telegram-bot
```


### Clone the repository

```console
$ cd /path/to/dir/
$ git clone https://github.com/PushDotGame/telegram-bots.git
```


### Make the `.env` file, then edit

```console
$ cp .env.sample .env
$ nano .env
```

Just edit it as:

```.env
SERVER_DOMAIN={server-ip}
SERVER_PORT=8443
CERT_DIR=/path/to/cert/dir
DATA_DIR=/path/to/data/dir
```

If your bot work behind a proxy, add:

```.env
PROXY_URL=http://{proxy-host}:{proxy-port}
```

or, follow [Working Behind a Proxy](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Working-Behind-a-Proxy)


### Make your bot configuration file

```console
$ cp .bot.sample /path/to/data/dir/.bot.{bot-session-name}
```

Edit it as:

```.env
BOT_TOKEN={bot-token}
BOT_PORT={bot-port}
```

For forward bot, you need:

```.env
FORWARD_CHAT_ID={telegram-chat-id}
```


### Self-signed certificate

Follow: [Creating a self-signed certificate using OpenSSL](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#creating-a-self-signed-certificate-using-openssl)

To create a self-signed SSL certificate using `openssl`, run the following command:

```console
$ openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 3650 -out cert.pem
```

Follow the promotes, you'll get `private.key` and `cert.pem`.

Move them to your cert directory:

```console
$ mv private.key /path/to/cert/dir
$ mv cert.pem /path/to/cert/dir
```

Limit the permission:

```console
$ sudo chmod 644 /path/to/cert/dir/*
```


### Make a system service for a bot

Use `fw2alice` as a `bot-session-name`,

create `/etc/systemd/system/bot-fw2alice.service`:

```
[Unit]
Description=TeleBOT fw2alice
After=network.target

[Service]
User={your-linux-username}
ExecStart=/usr/bin/python3 /path/to/telegram-bots/bot_fw.py fw2alice
Restart=on-abort

[Install]
WantedBy=multi-user.target
```


Enable it:

```console
$ sudo systemctl enable bot-fw2alice
```

Start it:

```console
$ sudo service bot-fw2alice start
```

Check the status:

```console
$ sudo service bot-fw2alice status
```


### Yeah, enjoy your bot.

<img style="width: 100%" src="https://raw.githubusercontent.com/PushDotGame/telegram-bots/master/clock.jpg" alt="enjoy-you-bot"/>



---

If you run more than one bot on your server,
read [Using nginx with one domain/port for all bots](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#using-nginx-with-one-domainport-for-all-bots)

And you may need:

### Nginx

Needed if multi-bots on your server. 

```console
$ sudo apt install nginx
```


### Create `/etc/nginx/sites-enabled/bots`

```
server {
    listen              {server-port, default: 8443} ssl;
    server_name         {server-ip, or domain};
    ssl_certificate     /path/to/cert.pem;
    ssl_certificate_key /path/to/private.key;

    location /{bot-id-1} {
        proxy_pass https://127.0.0.1:{bot-port-1}/{bot-id-1};
    }

    location /{bot-id-2} {
        proxy_pass https://127.0.0.1:{bot-port-2}/{bot-id-2};
    }
}
```

### Restart nginx

```console
$ sudo service nginx restart
```

...

Well done.
