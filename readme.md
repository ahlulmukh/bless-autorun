# Bless Auto Ping Nodes

This bot automates ping nodes bless

## Features

- Multi nodes
- Uses proxies to avoid IP bans/Limit.
- Bypass CF WAF

## Requirements

- Python [Download](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe).
- Bless Account [Register Here](https://bless.network/dashboard?ref=P3Z3OA).

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/ahlulmukh/bless-autorun.git
   cd bless-autorun
   ```

2. Make virtual env:

   ```sh
   python -m venv env

   pip install -r requirements.txt
   ```

3. Create a `proxy.txt` file in the root directory and add your proxies (one per line) (Optional).

   ```
   http://user:pass@host:port
   http://user:pass@host:port
   http://user:pass@host:port
   ```

4. Copy `accounts.json.example` to `accounts.json`.

change all with your detail

```
[
 {
     "Token": "Yourtoken",
     "Nodes": [
         {
             "PubKey": "pubkey1"
         },
         {
             "PubKey": "pubkey2"
         },
         {
             "PubKey": "pubkey3"
         },
         {
             "PubKey": "pubkey4"
         },
         {
             "PubKey": "pubkey5"
         }
     ]
 }
]
```

## Usage

1. Run the bot:

```sh
py main.py
```

## Stay Connected

- Channel Telegram : [Telegram](https://t.me/elpuqus)
- Channel WhatsApp : [Whatsapp](https://whatsapp.com/channel/0029VavBRhGBqbrEF9vxal1R)
- Discord : [Discord](https://discord.com/invite/uKM4UCAccY)

## Donation

If you would like to support the development of this project, you can make a donation using the following addresses:

- Solana: `6Y63evHexFANApfWEptqsJscyCgRG9PUZJwBncHbkKAU`
- EVM: `0xa3575c33814d5c4d07cee913a393a99a2a15867e`
- BTC: `bc1ppypst46a2wckpjd260kc4f8kkzf5w3u64wjlanudxezk0tyrts8sy26xs7`

## Disclaimer

This tool is for educational purposes only. Use it at your own risk.
