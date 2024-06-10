# Simple Service Pinger

SSP (Simple Service Pinger) is application for simplified checking availability of various services via these protocols:
* HTTP/HTTPS
* ICMP Echo
* TCP or UDP Socket!

It sends availability status of service via Telegram/E-Mail/Webhook and logging every check in stdout.

**To-Do:**
* Check availability via ICMP / TCP or UDP socket
* Make notifications via E-Mail / Webhook


## Usage

Fill `.env` file like that:

```
BOT_TOKEN = "1234567890:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # Take your bot token via @BotFather
CHAT_ID = "123456789" # group chat or private messages
```

Fill `service-list.yaml` like in sample:

```
- name: API Server example.com # Checks availability of https://example.com:443/api endpoint
  address: example.com
  port: 443
  protocol: https
  route: /api

- name: Google.com # Checks availability of http://google.com/ endpoint
  address: google.com
  port: 80
  protocol: http
```

Run your application!

```
python3 service-pinger.py
```
