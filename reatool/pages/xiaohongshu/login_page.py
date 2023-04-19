from PySide6.QtCore import Qt, Slot, QByteArray, Signal
from PySide6.QtGui import QPixmap, QShowEvent
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from reatool.core import GenerateQrcodeThread, CheckQrcodeThread


class LoginPage(QWidget):
    login_success = Signal(bool)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_widget = QLabel()
        logo_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_widget.setPixmap(QPixmap("asserts/xhs-logo.png"))
        layout.addWidget(logo_widget)
        layout.addSpacing(20)
        self.qrcode = QLabel("正在获取二维码中...")
        self.qrcode.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.qrcode)
        layout.addSpacing(20)
        self.qrcode_status = QLabel("")
        self.qrcode_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.qrcode_status)
        self.setLayout(layout)

        self.qrcode_thread = GenerateQrcodeThread()
        self.qrcode_thread.qrcode.connect(self.get_qrcode)

        self.check_qrcode_thread = CheckQrcodeThread()
        self.check_qrcode_thread.check_status.connect(self.check_qrcode)

    def showEvent(self, event: QShowEvent) -> None:
        print("logon page show")
        self.qrcode_thread.start()

    @Slot(dict)
    def get_qrcode(self, qrcode: dict):
        img_base64 = qrcode["base64"]
        print(img_base64)
        q_pixmap = QPixmap()
        q_pixmap.loadFromData(QByteArray.fromBase64(img_base64.encode()))
        self.qrcode.setPixmap(q_pixmap)
        self.check_qrcode_thread.qr_id = qrcode["qr_id"]
        self.check_qrcode_thread.qr_code = qrcode["code"]
        self.check_qrcode_thread.start()

    @Slot(dict)
    def check_qrcode(self, check_status: dict):
        code_status = check_status.get("code_status")
        self.qrcode_status.setText(check_status["msg"])
        if code_status == 2:
            self.login_success.emit(True)
