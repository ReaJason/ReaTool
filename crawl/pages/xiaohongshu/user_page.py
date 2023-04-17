import time

import requests
from PySide6.QtCore import QByteArray, Qt, Slot, Signal, QSize, QThread
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem, QResizeEvent, QFont
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QFormLayout, QLineEdit, QTableWidget, \
    QTableView, QAbstractItemView, QHeaderView, QTableWidgetItem

from crawl.core import GetSelfUserThread
from crawl.help import get_circle_image_from_url
from crawl.widget import Button, LineEdit


class UserPage(QWidget):
    fetch_success = Signal(bool)
    logout = Signal(bool)

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
        self.welcome_card.refresh_user_info.connect(self.get_self_info_thread.start)
        welcome_layout.addWidget(self.welcome_card)

        self.layout.addLayout(welcome_layout)
        self.layout.addSpacing(10)
        crawl_comments_card = CrawlComments()

        self.layout.addWidget(crawl_comments_card)

        self.get_self_info_thread.start()
        self.setLayout(self.layout)
        self.setStyleSheet("""

        QFrame {
           background-color: #ffffff;
            border-color: #d0d7de;
            border-radius: 6px;
            border-style: solid;
            border-width: 1px;
            margin: 0 30px;
        }

        QLabel{
            border: none;
            margin: 0;
        }

        QToolTip {
        border: none;
        margin: 0;
        }
        QHeaderView {
            margin: 0
        }

        """)

    @Slot(dict)
    def get_self_info(self, user):
        if not user:
            self.fetch_success.emit(False)
            return
        print(user)
        self.welcome_card.refresh(user)

    @Slot()
    def logout_success(self):
        print("退出登录")
        self.logout.emit(True)

    def resizeEvent(self, event: QResizeEvent) -> None:
        pass


class WelComeCard(QFrame):
    logout = Signal(bool)
    refresh_user_info = Signal(bool)

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.avatar = QLabel()
        self.avatar.setMinimumSize(80, 80)
        self.avatar.setMaximumSize(80, 80)
        layout.addWidget(self.avatar)
        layout.addSpacing(40)

        detail_info_layout = QVBoxLayout()
        detail_info_layout.setSpacing(0)
        detail_info_layout.setContentsMargins(0, 0, 0, 0)
        self.welcome_label = QLabel("Welcome!👋")
        self.welcome_label.setStyleSheet("""font-size: 16px; font-weight: bold""")
        self.user_info_label = QLabel()
        self.user_info_label.setStyleSheet("""font-size: 12px; color: #333; opacity:0.6;""")
        self.user_desc_label = QLabel()
        self.user_desc_label.setStyleSheet("""font-size: 12px; color: #333; opacity:0.6;""")
        self.user_desc_label.setWordWrap(True)
        detail_info_layout.addWidget(self.welcome_label)
        detail_info_layout.addWidget(self.user_info_label)
        detail_info_layout.addWidget(self.user_desc_label)
        layout.addLayout(detail_info_layout)

        refresh_button = Button("刷新信息")
        refresh_button.clicked.connect(self.refresh_clicked)

        logout_button = Button("登出")
        logout_button.clicked.connect(self.logout_clicked)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(0)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addWidget(refresh_button)
        button_layout.addSpacing(4)
        button_layout.addWidget(logout_button)

        layout.addLayout(button_layout)
        self.setFixedHeight(100)
        self.setLayout(layout)

    def refresh(self, user):
        basic_info = user["basic_info"]
        interactions = {interaction["type"]: interaction["count"] for interaction in user["interactions"]}
        self.welcome_label.setText(f"Welcome {basic_info['nickname']}！👋")
        self.user_info_label.setText(
            f"小红书号：{basic_info['red_id']}，"
            f"IP属地：{basic_info['ip_location']}，"
            f"关注：{interactions['follows']}，"
            f"粉丝：{interactions['fans']}，"
            f"获赞与收藏：{interactions['interaction']}")
        self.user_desc_label.setText("简介：" + basic_info["desc"])

        self.avatar.setPixmap(get_circle_image_from_url(basic_info["imageb"]))

    def logout_clicked(self):
        self.logout.emit(True)

    def refresh_clicked(self):
        self.refresh_user_info.emit(True)


class CrawlComments(QFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title_label = QLabel("指定笔记评论采集：")
        title_label.setStyleSheet("""font-size: 16px; font-weight: bold""")
        layout.addWidget(title_label)
        crawl_config_layout = QHBoxLayout()
        note_edit_widget = LineEdit()
        note_edit_widget.setPlaceholderText("请输入笔记ID")
        crawl_button = Button("开始采集")
        crawl_config_layout.addWidget(note_edit_widget)
        crawl_config_layout.addWidget(crawl_button)
        layout.addLayout(crawl_config_layout)

        self.crawl_display_table = QTableView()
        self.crawl_display_table.verticalHeader().hide()
        self.crawl_display_table.setShowGrid(False)
        self.crawl_display_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.crawl_display_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.crawl_display_table.setAlternatingRowColors(True)
        header = self.crawl_display_table.horizontalHeader()
        header.setHighlightSections(False)
        header.setSectionsClickable(False)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setFixedHeight(35)
        header_font = QFont()
        header_font.setPixelSize(14)
        header.setFont(header_font)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["评论用户昵称", "评论用户小红书 ID", "评论内容", "评论时间"])
        self.threads = MonitorThread()
        self.threads.row.connect(self.add_row_to_table)
        self.threads.start()

        self.crawl_display_table.setModel(self.model)
        self.crawl_display_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.crawl_display_table.resizeRowsToContents()
        self.crawl_display_table.setStyleSheet("""
        QTableView {
            border: 1px solid #d0d7de;
            border-radius: 6px;
            margin: 0
        }

        QHeaderView::section{
            background-color: #f6f8fa;
            font-weight: bold;
            border: none
        }
        QHeaderView::section:first {
            border-top-left-radius: 6px;
        }
        QHeaderView::section:last {
            border-top-right-radius: 6px;
        }
        QTableView::item {
            border-bottom: 1px solid hsla(210,18%,87%,1);
        }
""")

        layout.addWidget(self.crawl_display_table)
        self.setLayout(layout)
        self.setStyleSheet("""border: none;""")

    @Slot(dict)
    def add_row_to_table(self, row):
        items = []
        for j, (key, value) in enumerate(row.items()):
            item = QStandardItem(str(value))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setSizeHint(QSize(0, 35))
            font = QFont()
            font.setPixelSize(12)
            item.setFont(font)
            items.append(item)
        self.model.appendRow(items)
        self.crawl_display_table.scrollToBottom()


class MonitorThread(QThread):
    row = Signal(dict)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        while True:
            time.sleep(1)
            self.row.emit({"name": "John", "id": 123456789, "content": "12312111231231", "date": "2023-04-13", })
