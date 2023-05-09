import os
import queue

from PySide6.QtCore import Slot
from PySide6.QtGui import QStandardItemModel, Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QTableView

from reatool.core import download_path, GetNoteThread, NoteDownloadThread
from reatool.utils import show_error_message
from reatool.widget import Button, LineEdit, init_table
from reatool.widget.table import add_row_to_table


class CrawlNotes(QFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        tip = QLabel(
            "请在网页端打开笔记链接,也可将分享链接在网页打开。\n"
            "例如：https://www.xiaohongshu.com/explore/64425e520000000011010ca3 \n"
            "其中 64425e520000000011010ca3 即为笔记 ID")
        tip.setWordWrap(True)
        tip.setOpenExternalLinks(True)
        tip.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        tip.setStyleSheet("""
            padding: 20px 16px;
            font-size: 12px;
            background-color: #ddf4ff;
        """)
        layout.addWidget(tip)
        crawl_config_layout = QHBoxLayout()
        self.note_id_edit = LineEdit()
        self.note_id_edit.setPlaceholderText("请输入笔记ID")
        self.crawl_button = Button("开始")
        self.crawl_button.clicked.connect(self.start_crawl)
        crawl_config_layout.addWidget(self.note_id_edit)
        crawl_config_layout.addWidget(self.crawl_button)
        layout.addLayout(crawl_config_layout)

        self.crawl_display_table = QTableView()
        self.note_info = []
        init_table(self.crawl_display_table)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            ["ID", "博主", "博主ID", "标题", "内容", "点赞数", "评论数", "收藏数"])
        self.props = ["note_id", "user_name", "user_id", "title", "desc", "liked_count", "comment_count",
                      "collected_count"]
        self.crawl_display_table.setModel(self.model)
        self.user_save_path = download_path

        self.note_queue = queue.Queue()

        self.note_thread = GetNoteThread(self.note_queue)
        self.note_thread.note.connect(self.success_get_note)
        self.note_thread.error.connect(self.show_error)

        self.download_thread = NoteDownloadThread(self.note_queue)
        self.download_thread.complete.connect(self.end_download)

        layout.addWidget(self.crawl_display_table)
        self.setLayout(layout)
        self.setStyleSheet("""border: none;margin:0;""")

    @Slot(dict)
    def start_crawl(self, user):
        note_id = self.note_id_edit.text().strip()
        if note_id:
            self.crawl_button.setEnabled(False)
            self.crawl_button.setText("获取中...")
            self.note_id_edit.setEnabled(False)
            self.note_thread.note_id = note_id
            self.note_thread.start()
            self.download_thread.start()

    @Slot(str)
    def show_error(self, msg):
        show_error_message(msg)

    @Slot()
    def end_download(self):
        self.crawl_button.setEnabled(True)
        self.crawl_button.setText("开始")
        self.note_id_edit.setEnabled(True)

    @Slot(dict)
    def success_get_note(self, note):
        self.note_info.append(note)
        self.user_save_path = os.path.join(download_path, note["user_name"])
        add_row_to_table(self.model, self.props, note)
