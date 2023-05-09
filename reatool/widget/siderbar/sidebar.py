from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from .side_menu import SideMenuWidget
from reatool.__version__ import __title__


class SideBar(QWidget):
    def __init__(self, side_menus):
        super().__init__()

        self.side_menu_widget = SideMenuWidget(side_menus)

        layout = QVBoxLayout()
        logo_widget = QLabel()
        logo_widget.setText(__title__)
        logo_widget.setStyleSheet("""font-weight: bold;""")
        layout.addWidget(logo_widget)
        layout.addWidget(self.side_menu_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(200)
        self.setLayout(layout)
        self.setStyleSheet("""padding: 8px;border-right: 1px solid rgb(229, 231, 235);margin: 0px;border-radius: 0""")

    def set_current_row(self, row: int):
        self.side_menu_widget.setCurrentRow(row)

    def set_current_row_change(self, slot):
        self.side_menu_widget.currentRowChanged.connect(slot)
