import logging
import os

from PySide6.QtCore import QSettings
from .utils import get_cookie_from_local

root_path = os.path.abspath(".")
download_path = os.path.join(root_path, "download")
aria2_html_path = os.path.join(root_path, "aria2c.html")

if not os.path.exists(download_path):
    os.makedirs(download_path)


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
                local = get_cookie_from_local(domain_name=".xiaohongshu.com")
                logging.info(f"从本地加载 cookie 成功！，{local}")
                self.cookie = local
                return local
            except Exception as e:
                logging.error(f"从本地加载 cookie 失败, {e}")
                return ""
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
