import random

import requests

from src.utils.logger import Logger


class ProxyManager:
    def __init__(self, proxy_file="proxy.txt"):
        self.proxy_list = self.load_proxies(proxy_file)
        self.current_proxy = None

    def load_proxies(self, proxy_file):
        try:
            with open(proxy_file, "r") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("No proxies found in proxy file")
            Logger.log_message(
                None, None, f"Loaded {len(proxies)} proxies.", "success")
            return proxies
        except Exception as e:
            Logger.log_message(
                None, None, f"Error loading proxies: {str(e)}", "error")
            return []

    def get_random_proxy(self, index, total):
        if not self.proxy_list:
            Logger.log_message(
                index, total, "No proxies available. Using default IP.", "warning")
            self.current_proxy = None
            self.check_ip(index, total)
            return None

        self.current_proxy = random.choice(self.proxy_list)
        Logger.log_message(
            index, total, f"Using Proxy: {self.current_proxy}", "info")
        self.check_ip(index, total)
        return self.current_proxy

    def check_ip(self, index, total):
        proxy_dict = {
            "https": self.current_proxy} if self.current_proxy else None
        try:
            response = requests.get(
                "https://api64.ipify.org?format=json", proxies=proxy_dict, timeout=10)
            if response.status_code == 200:
                ip_address = response.json().get("ip", "Unknown IP")
                Logger.log_message(
                    index, total, f"IP Using: {ip_address}", "success")
            else:
                Logger.log_message(
                    index, total, "Failed to retrieve IP", "error")
        except Exception as e:
            Logger.log_message(
                index, total, f"Failed to get IP: {str(e)}", "error")
