from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from reatool.help import get_circle_image_from_url
from reatool.widget import Button


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
