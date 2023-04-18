import json

import requests

from . import TOKEN, RPC_URL


class Aria2Client:
    def __init__(self):
        pass

    @staticmethod
    def aria2_call(method, params=None):
        if params is None:
            params = []
        if params:
            params.insert(0, f"token:{TOKEN}")
        payload = {
            'jsonrpc': '2.0',
            "id": "",
            'method': method,
            'params': params
        }
        response = requests.post(RPC_URL, data=json.dumps(payload), headers={'content-type': 'application/json'})
        # print(response.text)
        return response.json().get('result')

    @staticmethod
    def add_url(uris, out_name, dir_path) -> str:
        return Aria2Client.aria2_call("aria2.addUri", [uris, {"out": out_name, "dir": dir_path}])

    @staticmethod
    def check_status(gid):
        return Aria2Client.aria2_call("aria2.tellStatus", [gid])

    @staticmethod
    def get_global_status():
        return Aria2Client.aria2_call("aria2.getGlobalStat")

    @staticmethod
    def get_active_info():
        return Aria2Client.aria2_call('aria2.tellActive')

    @staticmethod
    def shutdown():
        return Aria2Client.aria2_call("aria2.shutdown")
