import os
import sys

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from aria2.server import Aria2Server
from reatool import MainWidget

sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    app = QApplication()
    app.setStyle("fusion")
    app.setWindowIcon(QPixmap("asserts/logo.png"))
    Aria2Server.start()
    main_widget = MainWidget()
    main_widget.show()
    app.setStyleSheet("""
QWidget {
    background-color: #ffffff;
    font-size: 14px;
    font-weight: 500;
}""")

    sys.exit(app.exec())
