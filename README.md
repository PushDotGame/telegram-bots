# Telegram forward/id bot

## Bots 

### Forward bot 自动转发机器人

Auto forward every private message to a specific group or channel.

自动转发每一条私聊消息到一个特定的群组或频道


### Answer id bot 应答 ID 机器人

Example: [@answer_id_bot](https://t.me/answer_id_bot)

Answer the group/channel/user id, when you need.

当你需要时，给出群组/频道/用户的 ID



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


### Nginx

Needed if multi-bots on your server. 

```console
$ sudo apt install nginx
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

If you need a proxy, add:

```.env
PROXY_URL=http://{proxy-host}:{proxy-port}
```


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
