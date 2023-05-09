from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QTableView

from reatool.widget import LineEdit, Button, init_table


class CrawlComments(QFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        crawl_config_layout = QHBoxLayout()
        note_edit_widget = LineEdit()
        note_edit_widget.setPlaceholderText("请输入笔记ID")
        crawl_button = Button("开始采集")
        crawl_config_layout.addWidget(note_edit_widget)
        crawl_config_layout.addWidget(crawl_button)
        layout.addLayout(crawl_config_layout)

        self.crawl_display_table = QTableView()
        init_table(self.crawl_display_table)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["评论用户昵称", "评论用户小红书 ID", "评论内容", "评论时间"])
        self.crawl_display_table.setModel(self.model)

        layout.addWidget(self.crawl_display_table)
        self.setLayout(layout)
        self.setStyleSheet("""border: none;margin:0;""")
