from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


class Header(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.header_label = QLabel("header")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.header_label)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


