import json
import os
import queue

from PySide6.QtCore import QSize, Qt, Slot
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QTableView

from crawl.widget import Button, LineEdit, init_table
from crawl.core import GetUserNoteThread, NoteDownloadThread, GetUserThread


class CrawlUserNotes(QFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        crawl_config_layout = QHBoxLayout()
        self.user_id_edit = LineEdit()
        self.user_id_edit.setPlaceholderText("请输入用户ID")
        self.crawl_button = Button("开始采集")
        self.crawl_button.clicked.connect(self.get_user_info)
        crawl_config_layout.addWidget(self.user_id_edit)
        crawl_config_layout.addWidget(self.crawl_button)
        layout.addLayout(crawl_config_layout)

        self.crawl_display_table = QTableView()
        self.note_info = []
        init_table(self.crawl_display_table)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ID", "标题", "内容", "点赞数", "评论数", "收藏数", "状态"])
        self.props = ["note_id", "title", "desc", "liked_count", "comment_count", "collected_count", "status"]
        self.crawl_display_table.setModel(self.model)
        self.queue = queue.Queue()
        self.base_path = os.path.abspath('.')
        self.user_save_path = self.base_path
        self.user_note_thread = GetUserNoteThread(self.queue)
        self.user_note_thread.note.connect(self.success_get_note)
        self.user_info_thread = GetUserThread()
        self.user_info_thread.user.connect(self.start_crawl)

        self.download_thread = NoteDownloadThread(self.queue, self.base_path, 5)
        self.download_thread.info_index.connect(self.download_success)
        self.download_thread.error_index.connect(self.download_error)
        self.download_thread.complete.connect(self.end_crawl)

        layout.addWidget(self.crawl_display_table)
        self.setLayout(layout)
        self.setStyleSheet("""border: none;margin:0;""")

    @Slot(dict)
    def start_crawl(self, user):
        self.crawl_button.setEnabled(False)
        self.crawl_button.setText("爬取中...")
        self.user_id_edit.setEnabled(False)
        user_id = self.user_id_edit.text().strip()
        self.user_note_thread.user_id = user_id
        self.user_save_path = os.path.join(self.base_path, user["basic_info"]["nickname"])
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["ID", "标题", "内容", "点赞数", "评论数", "收藏数", "状态"])
        self.user_note_thread.start()
        self.download_thread.base_path = self.user_save_path
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
        self.crawl_button.setEnabled(True)
        self.crawl_button.setText("开始采集")
        self.user_id_edit.setEnabled(True)

    @Slot(dict)
    def success_get_note(self, note):
        self.note_info.append(note)
        self.add_row_to_table(note)

    @Slot(dict)
    def download_success(self, info_dict):
        index = info_dict["index"]
        info = info_dict["info"]
        if info:
            self.model.item(index, len(self.props) - 1).setText(info)

    @Slot(int)
    def download_error(self, index):
        self.model.item(index, len(self.props) - 1).setText("下载出错")

    def add_row_to_table(self, note):
        items = []
        for key in self.props:
            item = QStandardItem(str(note.get(key, "")))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setSizeHint(QSize(0, 35))
            font = QFont()
            font.setPixelSize(12)
            item.setFont(font)
            items.append(item)
        self.model.appendRow(items)
