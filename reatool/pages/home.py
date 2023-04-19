from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("你好"))
        layout.addWidget(QLabel("你好1"))
        layout.addWidget(QLabel("你好2"))
        self.setLayout(layout)
