from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QStackedLayout
from .login_page import LoginPage
from .user_page import UserPage
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
        self.user_page.logout.connect(self.logout)
        self.layout.addWidget(self.user_page)
        self.layout.addWidget(self.login_page)
        self.setLayout(self.layout)

    @Slot(bool)
    def login_success(self, success: bool):
        if success:
            self.layout.setCurrentWidget(self.user_page)
            self.user_page.get_self_info_thread.start()

    @Slot(bool)
    def get_user_success(self, success: bool):
        if not success:
            self.layout.setCurrentWidget(self.login_page)

    @Slot(bool)
    def logout(self, success: bool):
        if success:
            xiaohongshu_set_cookie("")
            self.layout.setCurrentWidget(self.login_page)