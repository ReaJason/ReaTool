from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QStandardItem
from PySide6.QtWidgets import QTableView, QAbstractItemView, QHeaderView


def init_table(table: QTableView):
    table.verticalHeader().hide()
    table.setShowGrid(False)
    table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
    table.setAlternatingRowColors(True)
    table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
    header = table.horizontalHeader()
    header.setHighlightSections(False)
    header.setSectionsClickable(False)
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    header.setFixedHeight(35)
    header_font = QFont()
    header_font.setPixelSize(14)
    header.setFont(header_font)
    table.setStyleSheet("""
            QTableView {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                margin: 0
            }

            QHeaderView::section{
                background-color: #f6f8fa;
                font-weight: bold;
                border: none
            }
            QHeaderView::section:first {
                border-top-left-radius: 6px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 6px;
            }
            QTableView::item {
                border-bottom: 1px solid hsla(210,18%,87%,1);
            }
    """)


def add_row_to_table(model, props, note):
    items = []
    for key in props:
        item = QStandardItem(str(note.get(key, "")))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setSizeHint(QSize(0, 35))
        font = QFont()
        font.setPixelSize(12)
        item.setFont(font)
        items.append(item)
    model.appendRow(items)
