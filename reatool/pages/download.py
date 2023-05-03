import os

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout
from reatool.core import root_path


class DownloadPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        web_engine = QWebEngineView()
        web_engine.load(QUrl.fromLocalFile(os.path.join(root_path, "aria2c.html")))
        layout.addWidget(web_engine)
        self.setLayout(layout)
