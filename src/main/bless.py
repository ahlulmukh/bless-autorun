import asyncio
import time
from datetime import datetime

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

    @staticmethod
    async def countdown(seconds: int) -> None:
        for remaining in range(seconds, 0, -1):
            Logger.log_message(
                message=f"Next ping in {remaining}s",
                message_type="warning",
                end='\r'
            )
            await asyncio.sleep(1)

        Logger.log_message(
            message="✓ Starting new ping, Please wait...",
            message_type="success"
        )

    async def get_node_data(self, auth_token):
        Logger.log_message(self.current_num, self.total,
                           "Trying to get data account", "process")
        try:
            url = "https://gateway-run-indexer.bls.dev/api/v1/nodes"
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "User-Agent": self.ua.random,
                "Content-Type": "application/json"
            }
            response = self.make_request_cs("GET", url, headers=headers)
            if response and response.status_code == 200:
                Logger.log_message(self.current_num, self.total,
                                   "Data account retrived succesfully", "success")
                return response.json()
            else:
                Logger.log_message(self.current_num, self.total,
                                   "failed to get node data", "error")
        except Exception as e:
            Logger.log_message(self.current_num, self.total,
                               f"Error getting node data: {str(e)}", "error")

    async def ping_node(self, nodes, auth_token):
        Logger.log_message(self.current_num, self.total,
                           f"Trying to ping node", "process")
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
                                   f"ping node {nodes.PubKey} !", "success")
            else:
                Logger.log_message(self.current_num, self.total,
                                   f"ping failed {nodes.PubKey}", "error")
        except Exception as e:
            Logger.log_message(self.current_num, self.total,
                               f"ping failed {nodes.PubKey} {str(e)}", "error")

    async def run_ping(self, account_data):
        Logger.log_message(self.current_num, self.total,
                           "Starting ping process", "process")
        token = account_data["Token"]
        nodes = account_data["Nodes"]

        for node in nodes:
            node_obj = type("Node", (object,), node)
            await self.ping_node(node_obj, token)

        data = await self.get_node_data(token)
        return {
            "totalReward": data[0].get("totalReward", 0),
            "todayReward": data[0].get("todayReward", 0),
        }
