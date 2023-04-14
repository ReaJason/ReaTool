from PySide6.QtCore import QSettings


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


XIAOHONGSHU = "xiaohongshu"

xiaohongshu_settings = Setting(XIAOHONGSHU)

XIAOHONGSHU_COOKIE = "cookie"


def xiaohongshu_set_cookie(value):
    xiaohongshu_settings.set_value(XIAOHONGSHU_COOKIE, value)


def xiaohongshu_get_cookie():
    return xiaohongshu_settings.get_value(XIAOHONGSHU_COOKIE)
