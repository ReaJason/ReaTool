from PySide6.QtWidgets import QLineEdit


class LineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""
        QLineEdit {
            padding: 5px 12px;
            font-size: 14px;
            line-height: 20px;
            color: #1F2328;
            vertical-align: middle;
            background-color: #f6f8fa;
            background-repeat: no-repeat;
            background-position: right 8px center;
            border: 1px solid #d0d7de;
            border-radius: 6px;
        }
        QLineEdit::focus {
            border-color: #0969da;
            outline: none;
            background-color: #ffffff;
        }
        """)
