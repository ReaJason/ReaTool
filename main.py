import os
import sys

from PySide6.QtWidgets import QApplication
from crawl import MainWidget
from aria2.server import Aria2Server

sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    app = QApplication()
    Aria2Server.start()
    main_widget = MainWidget()
    main_widget.show()
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    sys.exit(app.exec())
