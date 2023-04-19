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
            box-shadow: inset 0 1px 0 rgba(208,215,222,0.2);
            transition: 80ms cubic-bezier(0.33, 1, 0.68, 1);
            transition-property: color,background-color,box-shadow,border-color;
        }
        
        QLineEdit::focus {
            border-color: #0969da;
            outline: none;
            box-shadow: inset 0 0 0 1px transparent;
            background-color: #ffffff;
        }
        """)
