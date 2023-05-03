import logging

import requests
from PySide6.QtCore import QSettings
import browser_cookie3


class Setting:

    def __init__(self, prefix):
        self.prefix = prefix
        self.settings = QSettings("conf.ini", QSettings.Format.IniFormat)

    def set_value(self, key, value):
        self.settings.beginGroup(self.prefix)
        self.settings.setValue(key, value)
        self.settings.endGroup()

    def get_value(self, key):
        self.settings.beginGroup(self.prefix)
        value = self.settings.value(key)
        self.settings.endGroup()
        return value


def get_cookie_from_local():
    cj = browser_cookie3.load(domain_name=".xiaohongshu.com")
    cookie_dict = requests.utils.dict_from_cookiejar(cj)
    return ";".join([f"{key}={value}" for key, value in cookie_dict.items()])


class XhsSettings:

    def __init__(self):
        super().__init__()
        self.settings = Setting("xiaohongshu")
        self.cookie_key = "cookie"

    @property
    def cookie(self):
        value = self.settings.get_value(self.cookie_key)
        if not value:
            try:
                local = get_cookie_from_local() or "webId=1"
                logging.info(f"从本地加载 cookie 成功！，{local}")
                self.cookie = local
                return local
            except Exception as e:
                logging.error(f"从本地加载 cookie 失败, {e}")
                return "webId=1"
        return value

    @cookie.setter
    def cookie(self, cookie):
        self.settings.set_value(self.cookie_key, cookie)


class Aria2Settings:

    def __init__(self):
        super().__init__()
        self.settings = Setting("aria2")


xhs_settings = XhsSettings()
aria2_settings = Aria2Settings()
