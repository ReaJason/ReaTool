import requests
from PySide6.QtCore import QByteArray, Qt, Slot, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QWidget

from crawl.core import GetSelfUserThread
from crawl.help import get_circle_image_from_url
from crawl.widget import Button


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

        welcome_layout = QHBoxLayout()
        self.welcome_card = WelComeCard()
        self.welcome_card.logout.connect(self.logout_success)
        self.welcome_card.refresh_user_info.connect(self.get_self_info_thread.start)
        welcome_layout.addWidget(self.welcome_card)

        self.layout.addLayout(welcome_layout)
        self.get_self_info_thread.start()
        self.get_self_info_thread.user.connect(self.get_self_info)
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
        self.user_info_label = QLabel()
        self.user_info_label.setStyleSheet("""font-size: 12px; color: #333; opacity:0.6;""")
        self.user_desc_label = QLabel()
        self.user_desc_label.setStyleSheet("""font-size: 12px; color: #333; opacity:0.6;""")
        self.user_desc_label.setWordWrap(True)
        detail_info_layout.addWidget(self.welcome_label)
        detail_info_layout.addWidget(self.user_info_label)
        detail_info_layout.addWidget(self.user_desc_label)
        layout.addLayout(detail_info_layout)

        refresh_button = Button()
        refresh_button.setMaximumWidth(100)
        refresh_button.setText("刷新信息")
        refresh_button.clicked.connect(self.refresh_clicked)

        logout_button = Button()
        logout_button.setMaximumWidth(100)
        logout_button.setText("登出")
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
