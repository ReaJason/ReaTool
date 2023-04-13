from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from .side_menu import SideMenuWidget


class SideBar(QWidget):
    def __init__(self, side_menus):
        super().__init__()

        self.side_menu_widget = SideMenuWidget(side_menus)

        layout = QVBoxLayout()
        logo_widget = QLabel()
        logo_widget.setText("crawl spider")
        logo_widget.setStyleSheet("""font-weight: 700;""")

        # layout.addWidget(logo_widget)
        layout.addWidget(self.side_menu_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setStyleSheet("""
        background-color: rgb(249,250,251);
        padding: 8px;
        border-right: 1px solid rgb(229, 231, 235)
        """)

    def set_current_row(self, row: int):
        self.side_menu_widget.setCurrentRow(row)

    def set_current_row_change(self, slot):
        self.side_menu_widget.currentRowChanged.connect(slot)
