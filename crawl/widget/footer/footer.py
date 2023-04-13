from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from crawl.hitokoto_thread import HitokotoThread


class Footer(QWidget):
    def __init__(self, credit_label, version_label):
        super().__init__()

        layout = QHBoxLayout()
        credit_layout = QLabel(credit_label)
        credit_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.sentence_label = QLabel()
        self.sentence_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version_label = QLabel(version_label)
        version_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(credit_layout)
        layout.addWidget(self.sentence_label)
        layout.addWidget(version_label)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        self.setStyleSheet("""border-top: 1px solid rgb(229, 231, 235);""")
