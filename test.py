# http://sns-video-bd.xhscdn.com/pre_post/1000g0cg1rb643ggeu0005oldmvb6dbhtcpi0128  1.mp4
import json
import os.path
import subprocess
import time

import requests

# Set up JSON-RPC endpoint
url = 'http://localhost:6800/jsonrpc'
headers = {'content-type': 'application/json'}


# Call a method with specified parameters
def aria2_call(method, params=None):
    if params is None:
        params = []
    payload = {
        'jsonrpc': '2.0',
        "id": "",
        'method': method,
        'params': params
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(response.text)
    return response.json()['result']


# # Example usage: add a download
# gid = aria2_call('aria2.addUri', [['http://sns-video-bd.xhscdn.com/pre_post/1000g0cg1rb643ggeu0005oldmvb6dbhtcpi0128'],
#                                   {"out": "1.mp4"}])
#
#
# # while True:
# #     status = aria2_call('aria2.tellStatus', [gid])
# #     print(status)
#
#
class Aria2:
    TOKEN = "xhs_crawl"
    PORT = 6800

    def __init__(self):
        pass

    @classmethod
    def start(cls):
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
            f"--rpc-listen-port={cls.PORT}",
            f"--rpc-secret={cls.TOKEN}",
            f"--log={log_path}",
            f"--log-level={log_level}",
            f"--max-concurrent-downloads={max_concurrent_downloads}",
            f"--max-connection-per-server={max_connection_per_server}",
            f"--split={split}",
            f"--min-split-size={min_split_size}M",
            "--allow-overwrite=true",
            "--auto-file-renaming=false",
        ]
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(process)
        print(process.args)


# Aria2.start()
# gid = aria2_call('aria2.addUri', [f"token:{Aria2.TOKEN}",
#                                   ['http://sns-video-bd.xhscdn.com/pre_post/1000g0cg1rb643ggeu0005oldmvb6dbhtcpi0128'],
#                                   {"out": "1.mp4"}])
# aria2_call('aria2.addUri', [f"token:{Aria2.TOKEN}",
#                                   ['http://sns-video-bd.xhscdn.com/pre_post/1000g0cg1rb643ggeu0005oldmvb6dbhtcpi0128'],
#                                   {"out": "2.mp4"}])
# aria2_call('aria2.addUri', [f"token:{Aria2.TOKEN}",
#                                   ['http://sns-video-bd.xhscdn.com/pre_post/1000g0cg1rb643ggeu0005oldmvb6dbhtcpi0128'],
#                                   {"out": "3.mp4"}])
# aria2_call('aria2.addUri', [f"token:{Aria2.TOKEN}",
#                                   ['http://sns-video-bd.xhscdn.com/pre_post/1000g0cg1rb643ggeu0005oldmvb6dbhtcpi0128'],
#                                   {"out": "4.mp4"}])

# status = aria2_call('aria2.tellStatus', [f"token:xhs_crawl", "515775bcf6754f73"])
# status = aria2_call('aria2.getGlobalStat', ["token:xhs_crawl"])
# status = aria2_call('aria2.getGlobalOption', ["token:xhs_crawl"])
status = aria2_call('aria2.tellActive', ["token:xhs_crawl"])
# status = aria2_call('aria2.tellWaiting', ["token:xhs_crawl", 0, 10000])
# status = aria2_call('aria2.tellStopped', ["token:xhs_crawl", 0, 10000])
time.sleep(1)
print(status)
print(len(status))

# import subprocess
# import json
#
# # Command to start aria2 RPC server
# cmd = 'aria2c --enable-rpc --rpc-listen-all=true -D'
#
# # Start aria2 RPC server
# subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
#
# # Print the version
# print(f"aria2 version: {aria2_call('aria2.getVersion')}")
