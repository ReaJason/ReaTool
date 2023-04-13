from PySide6.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, style="default", *args, **kwargs):
        super().__init__(*args, **kwargs)
        default = style == "default"
        style_sheet = """
 QPushButton {
    border-radius: 6px;
    transition: 80ms cubic-bezier(0.33, 1, 0.68, 1);
    padding: 5px 16px;
    line-height: 20px;
    white-space: nowrap;
    vertical-align: middle;
    cursor: pointer;
    user-select: none;
    border-radius: 6px;
    appearance: none;
}

QPushButton:focus {
    outline: none;
}

QPushButton:pressed {
    transition: none;
    outline: none;
    box-shadow: none;
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
            box-shadow: 0 1px 0 rgba(27,31,36,0.04) , inset 0 1px 0 rgba(255,255,255,0.25);
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
            box-shadow: 0 1px 0 rgba(27,31,36,0.1),inset 0 1px 0 rgba(255,255,255,0.03);
            background-color: #0969da;
         }    
            """

        self.setStyleSheet(style_sheet)
