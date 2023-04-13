from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import QSettings, QDir
from crawl.widget import Button
from crawl.setting_manager import settings_manager

TIMEOUT = "timeout"
UA = "ua"
PREFIX = "requests"

DEFAULT_TIMEOUT = "5"
DEFAULT_UA = ("Mozilla/5.0 "
              "(Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 "
              "(KHTML, like Gecko) "
              "Chrome/111.0.0.0 Safari/537.36")


class SettingPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.timeout_edit = QLineEdit()

        form_layout.addRow("请求间隔", self.timeout_edit)

        self.ua_edit = QLineEdit()

        form_layout.addRow("用户代理", self.ua_edit)

        btn_layout = QHBoxLayout()
        button = Button(text="保存")
        button.clicked.connect(self.store_setting)
        btn_layout.addWidget(button)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.load_setting()
        self.setLayout(layout)

    def load_setting(self):
        settings_manager.beginGroup(PREFIX)
        self.timeout_edit.setText(settings_manager.value(TIMEOUT) or DEFAULT_TIMEOUT)
        self.ua_edit.setText(settings_manager.value(UA) or DEFAULT_UA)
        settings_manager.endGroup()

    def store_setting(self):
        settings_manager.beginGroup(PREFIX)
        settings_manager.setValue(TIMEOUT, self.timeout_edit.text())
        settings_manager.setValue(UA, self.ua_edit.text())
        settings_manager.endGroup()
