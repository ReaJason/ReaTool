from PySide6.QtCore import Qt, Slot, QByteArray, Signal
from PySide6.QtGui import QPixmap, QShowEvent
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from reatool.core import GenerateQrcodeThread, CheckQrcodeThread, GetSelfUserThread, xhs_settings, xhs_client
from reatool.utils import show_error_message
from reatool.widget import LineEdit, Button


class LoginPage(QWidget):
    login_success = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_widget = QLabel()
        logo_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_widget.setPixmap(QPixmap("asserts/xhs-logo.png"))
        layout.addWidget(logo_widget)
        layout.addSpacing(20)

        self.qrcode_thread = GenerateQrcodeThread()
        self.qrcode_thread.qrcode.connect(self.get_qrcode)
        self.qrcode_thread.error.connect(self.qr_code_error)

        self.check_qrcode_thread = CheckQrcodeThread()
        self.check_qrcode_thread.check_status.connect(self.check_qrcode)

        self.get_self_thread = GetSelfUserThread()
        self.get_self_thread.user.connect(self.validate_user)

        self.qrcode = QLabel("正在获取二维码中...")
        self.qrcode.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.qrcode)
        layout.addSpacing(10)
        self.qrcode_status = QLabel("")
        self.qrcode_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.qrcode_status)

        self.refresh_qrcode_button = Button("刷新二维码")
        self.refresh_qrcode_button.clicked.connect(self.refresh_qrcode)
        self.refresh_qrcode_button.setFixedWidth(200)
        layout.addWidget(self.refresh_qrcode_button)

        self.cookie_edit_line = LineEdit()
        self.cookie_edit_line.setPlaceholderText("请输入 Cookie")
        self.cookie_edit_line.setFixedWidth(200)
        self.cookie_login = Button("使用 Cookie 登录")
        self.cookie_login.setFixedWidth(200)
        self.cookie_login.clicked.connect(self.validate_cookie)

        layout.addWidget(self.cookie_edit_line)
        layout.addWidget(self.cookie_login)

        self.setLayout(layout)

    def showEvent(self, event: QShowEvent) -> None:
        self.qrcode_thread.start()

    def refresh_qrcode(self):
        self.qrcode.setText("正在获取二维码中...")
        self.check_qrcode_thread.quit()
        self.qrcode_thread.start()

    def validate_cookie(self):
        cookie = self.cookie_edit_line.text().strip()
        if cookie:
            try:
                xhs_client.cookie = cookie
                self.get_self_thread.start()
            except IndexError as e:
                show_error_message("请输入有效的 Cookie")

    @Slot(dict)
    def validate_user(self, user):
        if not user:
            xhs_client.cookie = ""
            self.qrcode_thread.start()
        else:
            xhs_settings.cookie = self.cookie_edit_line.text().strip()
            self.cookie_edit_line.setText("")
            self.check_qrcode_thread.exit()
            self.login_success.emit()

    @Slot(dict)
    def get_qrcode(self, qrcode: dict):
        img_base64 = qrcode["base64"]
        q_pixmap = QPixmap()
        q_pixmap.loadFromData(QByteArray.fromBase64(img_base64.encode()))
        self.qrcode.setPixmap(q_pixmap)
        self.check_qrcode_thread.qr_id = qrcode["qr_id"]
        self.check_qrcode_thread.qr_code = qrcode["code"]
        self.check_qrcode_thread.start()

    @Slot(str)
    def qr_code_error(self, error):
        self.qrcode.setText(error)

    @Slot(dict)
    def check_qrcode(self, check_status: dict):
        code_status = check_status.get("code_status")
        self.qrcode_status.setText(check_status["msg"])
        if code_status == 2:
            self.login_success.emit()
