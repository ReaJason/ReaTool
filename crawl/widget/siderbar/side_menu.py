from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QListWidgetItem, QListWidget


class SideMenuWidget(QListWidget):

    stylesheet = """
QListWidget {
    border: none;
    outline: 0;
    border-right: 1px solid rgb(229, 231, 235)
}

QListWidget::item {
    border-radius: 6px;
    margin-top: 4px;
    padding: 6px 8px 6px 8px;
}

QListWidget::item:selected {
    color: #FFFFFF;
    background-color: black;
}

QListWidget::item:focus {
    border: none;
}

QScrollBar:vertical {
            border: none;
            background:white;
            width:3px;
            margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));
    min-height: 0px;
}
QScrollBar::add-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));
    height: 0 px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}"""

    def __init__(self, menus):
        super().__init__()
        self.setStyleSheet(self.stylesheet)
        for menu in menus:
            item = QListWidgetItem(menu["label"])
            item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
            icon = QIcon()
            icon.addPixmap(QPixmap(menu["darkIcon"]), QIcon.Mode.Normal)
            icon.addPixmap(QPixmap(menu["lightIcon"]), QIcon.Mode.Selected)
            icon.addPixmap(QPixmap(menu["lightIcon"]), QIcon.Mode.Active)
            item.setIcon(icon)
            self.addItem(item)
