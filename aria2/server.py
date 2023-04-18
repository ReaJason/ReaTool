import os
import subprocess
from . import TOKEN, PORT
from .client import Aria2Client


class Aria2Server:
    def __init__(self):
        pass

    @staticmethod
    def start():
        aria2_exec_path = os.path.join(os.path.abspath("."), "aria2c.exe")
        aria2_path = os.path.join(os.path.abspath("."), "aria")
        if not os.path.exists(aria2_path):
            os.makedirs(aria2_path)
        log_path = os.path.join(aria2_path, "aria.log")
        if not os.path.exists(log_path):
            with open(log_path, "w"):
                pass

        # 日志级别 debug, info, notice, warn or error. 默认: debug
        log_level = "debug"
        # 最大同时下载数，默认为 5
        max_concurrent_downloads = "5"
        # 最大服务连接数，默认为 1
        max_connection_per_server = "1"
        # 单个文件最大线程数，默认为 5
        split = "5"
        # 最小分片大小
        min_split_size = "10"
        args = [
            aria2_exec_path,
            "--enable-rpc=true",
            "--rpc-allow-origin-all=true",
            "--rpc-listen-all=true",
            "--check-certificate=false",
            f"--rpc-listen-port={PORT}",
            f"--rpc-secret={TOKEN}",
            f"--log={log_path}",
            f"--log-level={log_level}",
            f"--max-concurrent-downloads={max_concurrent_downloads}",
            f"--max-connection-per-server={max_connection_per_server}",
            f"--split={split}",
            f"--min-split-size={min_split_size}M",
            "--allow-overwrite=true",
            "--auto-file-renaming=false",
            "-D"
        ]
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    def end():
        Aria2Client.shutdown()
