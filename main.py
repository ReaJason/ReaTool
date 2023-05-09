import os
import sys

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from reatool import MainWidget, InitWidget

sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    app = QApplication()
    app.setStyle("fusion")
    app.setWindowIcon(QPixmap("asserts/logo.png"))

    main_widget = MainWidget()
    init_widget = InitWidget(main_widget)
    init_widget.show()
    app.setStyleSheet("""
QFrame {
   background-color: #ffffff;
    border-color: #d0d7de;
    border-radius: 6px;
    border-style: solid;
    border-width: 1px;
    margin: 0 30px;
}

QLabel{
    border: none;
    margin: 0;
}

QToolTip {
    border: none;
    margin: 0;
}

QHeaderView {
    margin: 0
}

QWidget {
    background-color: #ffffff;
    font-size: 14px;
    font-weight: 500;
}

QTabWidget::pane {
    border: none;
}

QTabWidget::tab-bar {
    left: 32px
}

QTabBar::tab {
    border: none;
    padding: 5px 16px;
    margin: 0 4px;
}

QTabBar::tab:selected, QTabBar::tab:hover {
}

QTabBar::tab:selected {
    border-bottom: 2px solid #fd8c73;
}

QTabBar::tab:!selected {
    border-bottom: 2px solid transparent;
}""")

    sys.exit(app.exec())
