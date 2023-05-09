from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QTabWidget

from reatool.core import GetSelfUserThread
from .pages import CrawlNotes, CrawlUserNotes, CrawlAbout
from .welcome import WelComeCard


class UserPage(QWidget):
    fetch_success = Signal(bool)
    logout = Signal()

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.get_self_info_thread = GetSelfUserThread()
        self.get_self_info_thread.user.connect(self.get_self_info)

        welcome_layout = QHBoxLayout()
        self.welcome_card = WelComeCard()
        self.welcome_card.logout.connect(self.logout_success)
        welcome_layout.addWidget(self.welcome_card)

        self.layout.addLayout(welcome_layout)
        self.layout.addSpacing(10)

        tab_bar = QTabWidget()
        tab_bar.addTab(CrawlNotes(), "笔记详情")
        tab_bar.addTab(CrawlUserNotes(), "用户笔记")
        # tab_bar.addTab(CrawlComments(), "笔记评论")
        tab_bar.addTab(CrawlAbout(), "关于")
        self.layout.addWidget(tab_bar)

        self.get_self_info_thread.start()
        self.setLayout(self.layout)
        self.setStyleSheet("""

        

        """)

    @Slot(dict)
    def get_self_info(self, user):
        if not user:
            self.fetch_success.emit(False)
            return
        self.welcome_card.refresh(user)

    @Slot()
    def logout_success(self):
        self.logout.emit()

    def resizeEvent(self, event: QResizeEvent) -> None:
        pass






