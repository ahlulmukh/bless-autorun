import os
import random


class ProxyManager:
    def __init__(self, proxy_file="proxy.txt"):
        self.proxy_list = self.load_proxies(proxy_file)

    def load_proxies(self, proxy_file):
        if not os.path.exists(proxy_file):
            return []
        try:
            with open(proxy_file, "r") as f:
                proxies = [line.strip() for line in f if line.strip()]
            return proxies
        except:
            return []

    def get_random_proxy(self):
        if not self.proxy_list:
            return None
        return random.choice(self.proxy_list)
