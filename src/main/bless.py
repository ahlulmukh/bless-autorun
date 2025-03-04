import asyncio
import time

import cloudscraper
import requests
from fake_useragent import UserAgent

from src.utils.logger import Logger


class BlessAutoRun:
    def __init__(self, proxy=None, current_num=0, total=1):
        self.proxy = proxy
        self.current_num = current_num
        self.total = total
        self.session = requests.Session()
        self.ua = UserAgent()

    def make_request_cs(self, method, url, data=None, headers=None):
        scraper = cloudscraper.create_scraper()
        proxy_dict = {"https": self.proxy} if self.proxy else None
        for _ in range(3):
            try:
                headers = headers or {}
                headers["User-Agent"] = self.ua.random
                response = scraper.request(
                    method, url, json=data, headers=headers, proxies=proxy_dict, timeout=60
                )
                response.raise_for_status()
                return response
            except Exception as e:
                Logger.log_message(self.current_num, self.total,
                                   f"request failed: {str(e)}", "error")
                time.sleep(12)
        return None

    async def ping_node(self, nodes, auth_token):
        while True:
            try:
                url = f"https://gateway-run.bls.dev/api/v1/nodes/{nodes.PubKey}/ping"
                payload = {}
                headers = {
                    "Authorization": f"Bearer {auth_token}",
                    "User-Agent": self.ua.random,
                    "Content-Type": "application/json"
                }
                response = self.make_request_cs(
                    "POST", url, data=payload, headers=headers)

                if response and response.status_code == 200:
                    Logger.log_message(self.current_num, self.total,
                                       f"ping node {nodes.PubKey}", "success")
                else:
                    Logger.log_message(self.current_num, self.total,
                                       f"ping failed {nodes.PubKey}", "error")
            except Exception as e:
                Logger.log_message(self.current_num, self.total,
                                   f"ping failed {nodes.PubKey} {str(e)}", "error")
            await asyncio.sleep(600)
