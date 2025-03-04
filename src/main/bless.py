import asyncio
from datetime import datetime, timedelta

import cloudscraper
import requests
from fake_useragent import UserAgent


class BlessAutoRun:
    def __init__(self, proxy_manager):
        self.proxy_manager = proxy_manager
        self.ua = UserAgent()

    def _get_ip(self, proxy):
        try:
            proxy_dict = {"https": proxy} if proxy else None
            r = requests.get("https://api64.ipify.org?format=json",
                             proxies=proxy_dict, timeout=10)
            if r.status_code == 200:
                return r.json().get("ip", "Unknown")
        except:
            pass
        return "Failed"

    def _ping_one_pubkey(self, token, pubkey, proxy):
        url = f"https://gateway-run.bls.dev/api/v1/nodes/{pubkey}/ping"
        scraper = cloudscraper.create_scraper()
        proxy_dict = {"https": proxy} if proxy else None

        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": self.ua.random,
            "Content-Type": "application/json"
        }
        try:
            resp = scraper.post(url, json={}, headers=headers,
                                proxies=proxy_dict, timeout=60)
            if resp and resp.status_code == 200:
                return True
        except:
            pass
        return False

    async def ping_account_loop(self, account_dict, interval):
        token = account_dict["token"]
        nodes = account_dict["nodes"]

        while True:
            proxy = self.proxy_manager.get_random_proxy()
            ip_current = self._get_ip(proxy)
            for node in nodes:
                node["ping_status"] = "On Ping"
            for node in nodes:
                pub = node["pubkey"]
                ok = self._ping_one_pubkey(token, pub, proxy)
                if ok:
                    node["ping_status"] = "OK"
                else:
                    node["ping_status"] = "Failed"

                node["last_ping"] = datetime.now().strftime("%H:%M:%S")
                node["ip"] = ip_current
                node["_next_ping"] = datetime.now(
                ) + timedelta(seconds=interval)

            await asyncio.sleep(interval)
