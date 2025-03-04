import asyncio
from datetime import datetime

import keyboard
from rich import box
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table


class TableView:
    def __init__(self, accounts_data, ping_interval=600):
        self.accounts_data = accounts_data
        self.ping_interval = ping_interval
        self.selected_account_index = 0
        self.refresh_table_interval = 1
        self.console = Console()
        self.screen_mode = True

    def build_ascii_banner(self):
        banner = r"""
░█▀▄░█░░░█▀▀░█▀▀░█▀▀
░█▀▄░█░░░█▀▀░▀▀█░▀▀█
░▀▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀
By : El Puqus Airdrop
github.com/ahlulmukh
Press <UP> / <DOWN> to switch account.
        """
        return Panel(
            banner,
            box=box.MINIMAL,
        )

    def build_table(self):
        total_accounts = len(self.accounts_data)
        current_number = self.selected_account_index + 1
        table = Table(
            title=f"[bold magenta]Account #{current_number} / {total_accounts}[/bold magenta]",
            show_lines=True,
            box=box.ROUNDED,
            border_style="cyan",
            expand=True,
        )

        table.add_column("No", justify="right")
        table.add_column("Token")
        table.add_column("PubKey")
        table.add_column("Ping")
        table.add_column("Last Ping")
        table.add_column("Countdown", justify="center")
        table.add_column("IP Using")
        if not self.accounts_data:
            return table
        if self.selected_account_index >= len(self.accounts_data):
            return table

        now = datetime.now()
        account_data = self.accounts_data[self.selected_account_index]
        token = account_data.get("token", "")
        nodes = account_data.get("nodes", [])

        for i, nd in enumerate(nodes, start=1):
            pubkey = nd.get("pubkey", "")
            ping_stat = nd.get("ping_status", "Init")
            last_ping = nd.get("last_ping", "-")
            ip_now = nd.get("ip", "-")

            cd_str = "-"
            next_ping = nd.get("_next_ping")
            if next_ping:
                delta = (next_ping - now).total_seconds()
                cd_str = str(int(delta)) if delta > 0 else "0"

            if ping_stat == "OK":
                ping_str = f"[green]{ping_stat}[/green]"
            elif ping_stat == "On Ping":
                ping_str = f"[yellow]{ping_stat}[/yellow]"
            elif ping_stat == "Failed":
                ping_str = f"[red]{ping_stat}[/red]"
            else:
                ping_str = ping_stat

            table.add_row(
                str(i),
                token,
                pubkey,
                ping_str,
                last_ping,
                cd_str,
                ip_now
            )

        return table

    async def live_update_table(self):
        with Live(console=self.console, screen=self.screen_mode, refresh_per_second=2) as live:
            while True:
                banner_panel = self.build_ascii_banner()
                table = self.build_table()
                layout_group = Group(banner_panel, table)

                live.update(layout_group)
                await asyncio.sleep(self.refresh_table_interval)

    def handle_keypress_up(self):
        self.selected_account_index = max(0, self.selected_account_index - 1)

    def handle_keypress_down(self):
        max_idx = len(self.accounts_data) - 1
        self.selected_account_index = min(
            max_idx, self.selected_account_index + 1)

    async def keyboard_loop(self):
        while True:
            if keyboard.is_pressed("up"):
                self.handle_keypress_up()
            if keyboard.is_pressed("down"):
                self.handle_keypress_down()

            await asyncio.sleep(0.1)
