from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QStackedLayout
from .login_page import LoginPage
from .user_page import UserPage
from reatool.setting_manager import xhs_settings
from reatool.core import xhs_client


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

    @Slot()
    def login_success(self):
        self.layout.setCurrentWidget(self.user_page)
        self.user_page.get_self_info_thread.start()

    @Slot(bool)
    def get_user_success(self, success: bool):
        if not success:
            self.layout.setCurrentWidget(self.login_page)

    @Slot()
    def logout(self):
        xhs_settings.cookie = ""
        xhs_client.session.cookies.clear()
        xhs_client.cookie = "webId=1"
        self.layout.setCurrentWidget(self.login_page)
