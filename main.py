import os
import sys
from PySide6.QtWidgets import QApplication
from reatool import MainWidget
from aria2.server import Aria2Server
import reatool.log

sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    app = QApplication()
    app.setStyle("fusion")
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
