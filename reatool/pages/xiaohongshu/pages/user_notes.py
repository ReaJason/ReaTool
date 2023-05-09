import json
import os
import queue

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QTableView

from reatool.core import download_path, GetUserNoteThread, GetUserThread, NoteDownloadThread
from reatool.utils import show_error_message
from reatool.widget import LineEdit, Button, init_table
from reatool.widget.table import add_row_to_table


class CrawlUserNotes(QFrame):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        tip = QLabel(
            "请在网页端打开用户主页。\n"
            "例如：https://www.xiaohongshu.com/user/profile/63273a77000000002303cc9b\n"
            "其中 63273a77000000002303cc9b 即为博主 ID")
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
        self.user_id_edit = LineEdit()
        self.user_id_edit.setPlaceholderText("请输入博主ID")
        self.crawl_button = Button("开始")

        self.crawl_button.clicked.connect(self.get_user_info)

        crawl_config_layout.addWidget(self.user_id_edit)
        crawl_config_layout.addWidget(self.crawl_button)
        layout.addLayout(crawl_config_layout)

        self.crawl_display_table = QTableView()
        self.note_info = []
        self.user_save_path = download_path
        init_table(self.crawl_display_table)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ID", "标题", "内容", "点赞数", "评论数", "收藏数"])
        self.props = ["note_id", "title", "desc", "liked_count", "comment_count", "collected_count"]
        self.crawl_display_table.setModel(self.model)
        self.note_queue = queue.Queue()
        self.crawl_completed = False
        self.user_note_thread = GetUserNoteThread(self.note_queue)
        self.user_note_thread.note.connect(self.success_get_note)
        self.user_note_thread.error.connect(self.show_error)
        self.user_note_thread.completed.connect(self.end_crawl)
        self.user_info_thread = GetUserThread()
        self.user_info_thread.user.connect(self.start_crawl)
        self.user_info_thread.error.connect(self.show_error)

        self.download_thread = NoteDownloadThread(self.note_queue)
        self.download_thread.complete.connect(self.end_download)

        layout.addWidget(self.crawl_display_table)
        self.setLayout(layout)
        self.setStyleSheet("""border: none;margin:0;""")

    @Slot(dict)
    def start_crawl(self, user):
        self.crawl_button.setEnabled(False)
        self.crawl_completed = False
        self.crawl_button.setText("获取中...")
        self.user_id_edit.setEnabled(False)
        user_id = self.user_id_edit.text().strip()
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["ID", "标题", "内容", "点赞数", "评论数", "收藏数"])
        self.user_note_thread.user_id = user_id
        self.user_note_thread.start()
        self.download_thread.start()

    @Slot()
    def get_user_info(self):
        self.note_info = []
        user_id = self.user_id_edit.text().strip()
        if user_id:
            self.user_info_thread.user_id = user_id
            self.user_info_thread.start()

    @Slot()
    def end_crawl(self):
        with open(os.path.join(self.user_save_path, f"{self.user_id_edit.text().strip()}.json"), "w",
                  encoding="utf-8") as f:
            json.dump(self.note_info, f, ensure_ascii=False, indent=4)
        self.crawl_completed = True
        self.end_download()

    @Slot(str)
    def show_error(self, msg):
        show_error_message(msg)

    @Slot()
    def end_download(self):
        if self.crawl_completed:
            self.crawl_button.setEnabled(True)
            self.crawl_button.setText("开始")
            self.user_id_edit.setEnabled(True)

    @Slot(dict)
    def success_get_note(self, note):
        self.note_info.append(note)
        self.user_save_path = os.path.join(download_path, note["user_name"])
        item = self.model.findItems(note["note_id"], Qt.MatchFlag.MatchExactly)
        if not len(item):
            add_row_to_table(self.model, self.props, note)
