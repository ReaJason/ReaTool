from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class AboutPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("关于"))
        self.setLayout(layout)
