from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import QSettings, QDir
from reatool.widget import Button


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
        btn_layout.addWidget(button)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
