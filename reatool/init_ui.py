from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from .log import init_log
from .main_ui import MainWidget
import logging
from aria2.server import Aria2Server


class InitThread(QThread):
    msg = Signal(str)
    completed = Signal()

    def __init__(self, parent):
        super().__init__()
        self.parent_widget = parent

    def run(self) -> None:
        self.msg.emit("正在初始化日志服务......")
        init_log()
        logging.info("初始化日志服务成功")
        self.msg.emit("正在初始化 aria2......")
        Aria2Server.start()
        version = Aria2Server.get_version()
        logging.info(f"初始化 aria2 {version['version']} 成功!")
        self.msg.emit(f"aria2 {version['version']} 启动成功")
        self.completed.emit()
        logging.info("初始化完成")


class InitWidget(QWidget):
    def __init__(self, main_widget: MainWidget):
        super().__init__()
        self.main_widget = main_widget
        self.setFixedSize(300, 200)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        layout = QVBoxLayout(self)
        widget = QWidget()
        widget.setStyleSheet("""
        background-color: #e4866a;
        border-radius: 6px;
        """)
        widget_layout = QVBoxLayout(widget)
        widget_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label = QLabel("👋 Welcome to ReaTool!")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)
        widget_layout.addWidget(title_label)
        self.label = QLabel("正在初始化中......")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget_layout.addWidget(self.label)

        self.init_thread = InitThread(self)
        self.init_thread.msg.connect(self.show_msg)
        self.init_thread.completed.connect(self.init_completed)
        self.init_thread.start()

        layout.addWidget(widget)
        self.setLayout(layout)

    @Slot(str)
    def show_msg(self, msg):
        self.label.setText(msg)

    @Slot()
    def init_completed(self):
        self.close()
        self.main_widget.init_ui()
        self.main_widget.show()
