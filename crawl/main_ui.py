from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QStackedLayout, QHBoxLayout, QVBoxLayout

from .__version__ import __version__, __title__, __copyright__
from .hitokoto_thread import HitokotoThread
from .pages import HomePage, XiaohongshuPage
from .widget import SideBar, Footer
from aria2.server import Aria2Server


class MainWidget(QWidget):
    side_menu = [
        {
            "label": "首页",
            "lightIcon": "asserts/home-light.png",
            "darkIcon": "asserts/home-dark.png",
            "pageWidget": HomePage,
        },
        {
            "label": "小红书爬虫",
            "lightIcon": "asserts/spider-light.png",
            "darkIcon": "asserts/spider-dark.png",
            "pageWidget": XiaohongshuPage,
        },
    ]

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.resize(1280, 720)
        self.setMinimumSize(1280, 720)
        self.setWindowTitle(__title__)
        self.setWindowIcon(QPixmap("asserts/logo.png"))

        menu_widget = SideBar(self.side_menu)

        # 默认显示打开首页
        menu_widget.set_current_row(0)

        menu_widget.setFixedWidth(200)
        menu_widget.set_current_row_change(self.page_change)

        main_widget = QVBoxLayout()

        # header_widget = Header()
        self.footer_widget = Footer(__copyright__, __version__)

        self.page_layout = QStackedLayout()
        for menu in self.side_menu:
            self.page_layout.addWidget(menu.get("pageWidget")())

        # main_widget.addWidget(header_widget)
        main_widget.addLayout(self.page_layout)
        main_widget.addWidget(self.footer_widget)
        main_widget.setSpacing(0)
        main_widget.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(menu_widget)
        layout.addLayout(main_widget)
        self.setLayout(layout)

        self.thread = HitokotoThread()
        self.thread.text_signal.connect(self.update_label)
        self.thread.start()

    @Slot(str)
    def page_change(self, current_row: int):
        self.page_layout.setCurrentIndex(current_row)

    @Slot(str)
    def update_label(self, sentence):
        self.footer_widget.sentence_label.setText(sentence)

    def closeEvent(self, event) -> None:
        Aria2Server.end()
