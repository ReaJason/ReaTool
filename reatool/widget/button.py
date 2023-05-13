from PySide6.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, *args, style="default", **kwargs):
        super().__init__(*args, **kwargs)
        default = style == "default"
        self.setMaximumWidth(100)
        self.setMinimumWidth(100)
        style_sheet = """
 QPushButton {
    border-radius: 6px;
    padding: 5px 16px;
    line-height: 20px;
    white-space: nowrap;
    vertical-align: middle;
    border-radius: 6px;
}

QPushButton:focus {
    outline: none;
}

QPushButton:pressed {
    outline: none;
    text-decoration: none;
}

QPushButton:flat {
        border: none;
}
        """

        if default:
            style_sheet += """
         QPushButton {
            color: #24292f;
            border: 1px solid rgba(27,31,36,0.15);
            background-color: #f6f8fa;
         }
        QPushButton:pressed {
            background-color: hsla(220,14%,93%,1);
            border-color: rgba(27,31,36,0.15);
        }
            """
        else:
            style_sheet += """
         QPushButton {
            color: "#ffffff";
            border: 1px solid rgba(27,31,36,0.15);
            background-color: #0969da;
         }
            """

        self.setStyleSheet(style_sheet)
