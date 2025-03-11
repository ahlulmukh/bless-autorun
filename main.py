import asyncio
import json
import os
from datetime import datetime

from src.main.bless import BlessAutoRun
from src.main.proxy import ProxyManager
from src.utils.logger import Logger


def load_accounts(filename="accounts.json"):
    if not os.path.exists(filename):
        Logger.log_message(0, 0, "accounts.json not found", "error")
        return []
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        Logger.log_message(0, 0, "Error accounts.json", "error")
        return []


async def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("""
 ░█▀▄░█░░░█▀▀░█▀▀░█▀▀
 ░█▀▄░█░░░█▀▀░▀▀█░▀▀█
 ░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀
         By : El Puqus Airdrop
         github.com/ahlulmukh
    """)

    proxy_manager = ProxyManager()
    accounts = load_accounts()
    if not accounts:
        return

    try:
        while True:

            results = []
            for i, account in enumerate(accounts):
                try:
                    print("─" * 70)
                    proxy = proxy_manager.get_random_proxy(
                        i + 1, len(accounts))
                    bot = BlessAutoRun(
                        proxy=proxy, current_num=i + 1, total=len(accounts))
                    result = await bot.run_ping(account)
                    results.append(result)
                except Exception as e:
                    Logger.log_message(
                        i + 1, len(accounts), f"Failed to process account: {str(e)}", "error")
                    results.append({
                        "totalReward": 0,
                        "todayReward": 0,
                        "nodes": []
                    })
            print('\n')
            Logger.log_message(0, 0, "Accounts List", "success")
            print("═" * 70)
            for result in results:
                Logger.log_message(
                    0, 0, f"Total Reward: {result['totalReward']}", "success")
                Logger.log_message(
                    0, 0, f"Today Reward: {result['todayReward']}", "success")
                print("─" * 70)

            await bot.countdown(600)

    except KeyboardInterrupt:
        Logger.log_message(0, 0, "Process interrupted by user", "warning")
    except Exception as e:
        Logger.log_message(0, 0, f"Fatal error: {str(e)}", "error")


if __name__ == "__main__":
    asyncio.run(main())
