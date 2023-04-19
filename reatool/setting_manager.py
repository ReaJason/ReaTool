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


class XhsSettings:

    def __init__(self):
        super().__init__()
        self.settings = Setting("xiaohongshu")
        self.cookie_key = "cookie"

    @property
    def cookie(self):
        value = self.settings.get_value(self.cookie_key)
        return value

    @cookie.setter
    def cookie(self, cookie):
        self.settings.set_value(self.cookie_key, cookie)


xhs_settings = XhsSettings()
