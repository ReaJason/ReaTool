from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from crawl.setting_manager import settings_manager


class SpiderPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("爬虫"))
        self.setLayout(layout)
