import json
import logging
import requests

from . import TOKEN, RPC_URL


class Aria2Client:
    def __init__(self):
        pass

    @staticmethod
    def aria2_call(method, params=None):
        token_str = f"token:{TOKEN}"
        if params is None:
            params = [token_str]
        if params:
            params.insert(0, token_str)
        payload = {
            'jsonrpc': '2.0',
            "id": "",
            'method': method,
            'params': params
        }
        response = requests.post(RPC_URL, data=json.dumps(payload), headers={'content-type': 'application/json'})
        logging.debug(response.text)
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

    @staticmethod
    def force_shutdown():
        return Aria2Client.aria2_call("aria2.forceShutdown")

    @staticmethod
    def get_version():
        return Aria2Client.aria2_call("aria2.getVersion")
