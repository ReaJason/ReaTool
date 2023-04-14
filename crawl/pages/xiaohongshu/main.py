from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QStackedLayout
from .login_page import LoginPage
from crawl.core import GetSelfUserThread
from crawl.setting_manager import xiaohongshu_set_cookie


class XiaohongshuPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QStackedLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.login_page = LoginPage()
        self.login_page.login_success.connect(self.login_success)
        self.user_page = UserPage()
        self.user_page.fetch_success.connect(self.get_user_success)
        self.layout.addWidget(self.user_page)
        self.layout.addWidget(self.login_page)
        self.setLayout(self.layout)

    @Slot(bool)
    def login_success(self, success: bool):
        if success:
            self.layout.setCurrentWidget(self.user_page)

    @Slot(bool)
    def get_user_success(self, success: bool):
        if not success:
            self.layout.setCurrentWidget(self.login_page)


class UserPage(QWidget):
    fetch_success = Signal(bool)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("主页"))
        self.get_self_info_thread = GetSelfUserThread()
        self.get_self_info_thread.start()
        self.get_self_info_thread.user.connect(self.get_self_info)
        self.setLayout(self.layout)

    @Slot(dict)
    def get_self_info(self, user):
        if not user:
            self.fetch_success.emit(False)
            return
        print(user)
