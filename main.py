import asyncio
import json
import os

from src.main.bless import BlessAutoRun
from src.main.proxy import ProxyManager
from src.main.table import TableView

ACCOUNTS_FILE = "accounts.json"
PROXY_FILE = "proxy.txt"
PING_INTERVAL = 600

ACCOUNTS_DATA = []

proxy_manager = ProxyManager(PROXY_FILE)


def load_accounts(filename=ACCOUNTS_FILE):
    if not os.path.exists(filename):
        print(f"[Error] {filename} not found.")
        return []
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Error] Failed read file {filename}: {e}")
        return []


async def main():
    accounts_json = load_accounts()
    if not accounts_json:
        print("[Info] No account.json.")
        return
    global ACCOUNTS_DATA
    for acc in accounts_json:
        token = acc.get("Token", "")
        nodes_data = acc.get("Nodes", [])
        node_dicts = []
        for nd in nodes_data:
            pub = nd.get("PubKey", "")
            node_dicts.append({
                "pubkey": pub,
                "ping_status": "Init",
                "last_ping": "-",
                "ip": "-",
                "_next_ping": None
            })
        account_dict = {"token": token, "nodes": node_dicts}
        ACCOUNTS_DATA.append(account_dict)
    tasks = []
    for acc_dict in ACCOUNTS_DATA:
        bless = BlessAutoRun(proxy_manager)
        t = asyncio.create_task(
            bless.ping_account_loop(acc_dict, PING_INTERVAL))
        tasks.append(t)

    table_view = TableView(ACCOUNTS_DATA, ping_interval=PING_INTERVAL)
    table_task = asyncio.create_task(table_view.live_update_table())
    kb_task = asyncio.create_task(table_view.keyboard_loop())
    await asyncio.gather(table_task, kb_task, *tasks)

if __name__ == "__main__":
    asyncio.run(main())
