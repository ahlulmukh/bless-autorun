from datetime import datetime

from colorama import Fore, Style, init

init(autoreset=True)


class Logger:
    @staticmethod
    def log_message(current_num=None, total=None, message="", message_type="info", end="\n"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        account_status = f"[{current_num}/{total}] " if current_num and total else ""

        colors = {
            "info": Fore.WHITE,
            "success": Fore.GREEN,
            "error": Fore.RED,
            "warning": Fore.YELLOW,
            "process": Fore.CYAN,
            "debug": Fore.BLUE,
        }

        color = colors.get(message_type, Fore.WHITE)
        print(
            f"{Fore.WHITE}[{timestamp}] {account_status}{color}{message}{Style.RESET_ALL}", end=end
        )
