from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QStackedLayout, QHBoxLayout, QVBoxLayout, QMessageBox

from aria2.server import Aria2Server
from .__version__ import __version__, __title__, __copyright__
from .pages import XiaohongshuPage
from .widget import SideBar, Footer


class MainWidget(QWidget):
    side_menu = [
        # {
        #     "label": "首页",
        #     "lightIcon": "asserts/home-light.png",
        #     "darkIcon": "asserts/home-dark.png",
        #     "pageWidget": HomePage,
        # },
        {
            "label": "小红书",
            "lightIcon": "asserts/spider-light.png",
            "darkIcon": "asserts/spider-dark.png",
            "pageWidget": XiaohongshuPage,
        },
    ]

    def __init__(self):
        super().__init__()
        self.page_layout = None
        self.resize(1280, 720)
        self.setMinimumSize(1280, 720)
        self.setWindowTitle(__title__)

    def init_ui(self):
        menu_widget = SideBar(self.side_menu)

        # 默认显示打开首页
        menu_widget.set_current_row(0)
        menu_widget.set_current_row_change(self.page_change)

        main_widget = QVBoxLayout()

        # header_widget = Header()
        footer_widget = Footer(__copyright__, __version__)

        self.page_layout = QStackedLayout()
        for menu in self.side_menu:
            self.page_layout.addWidget(menu.get("pageWidget")())

        # main_widget.addWidget(header_widget)
        main_widget.addLayout(self.page_layout)
        main_widget.addWidget(footer_widget)
        main_widget.setSpacing(0)
        main_widget.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(menu_widget)
        layout.addLayout(main_widget)
        self.setLayout(layout)

    @Slot(str)
    def page_change(self, current_row: int):
        self.page_layout.setCurrentIndex(current_row)

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, '关闭',
                                     "确认关闭吗?", QMessageBox.StandardButton.Ok |
                                     QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Ok:
            event.accept()
            Aria2Server.end()
        else:
            event.ignore()
