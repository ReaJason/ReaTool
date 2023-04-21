import json
import logging
import os
import queue
import subprocess

from PySide6.QtCore import QSize, Qt, Slot
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QTableView, QMessageBox, QFileDialog, QLabel

from reatool.widget import Button, LineEdit, init_table
from reatool.core import GetUserNoteThread, NoteDownloadThread, GetUserThread, DownloadCheckThread, download_path, \
    GetNoteThread


def show_error(msg):
    QMessageBox.critical(None, '错误', msg, QMessageBox.StandardButton.Close)


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
        open_download_path_button = Button("打开下载文件夹")
        open_download_path_button.clicked.connect(self.open_download_path)
        open_download_path_button.setFixedWidth(150)
        self.crawl_button.clicked.connect(self.get_user_info)
        crawl_config_layout.addWidget(self.user_id_edit)
        crawl_config_layout.addWidget(self.crawl_button)
        crawl_config_layout.addWidget(open_download_path_button)
        layout.addLayout(crawl_config_layout)

        self.crawl_display_table = QTableView()
        self.note_info = []
        self.user_save_path = download_path
        init_table(self.crawl_display_table)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ID", "标题", "内容", "点赞数", "评论数", "收藏数", "状态"])
        self.props = ["note_id", "title", "desc", "liked_count", "comment_count", "collected_count", "status"]
        self.crawl_display_table.setModel(self.model)
        self.note_queue = queue.Queue()
        self.user_note_thread = GetUserNoteThread(self.note_queue)
        self.user_note_thread.note.connect(self.success_get_note)
        self.user_info_thread = GetUserThread()
        self.user_info_thread.user.connect(self.start_crawl)
        self.user_info_thread.error.connect(self.show_error)

        self.download_queue = queue.Queue()

        self.download_thread = NoteDownloadThread(self.note_queue, self.download_queue)
        self.download_thread.complete.connect(self.end_crawl)

        self.download_check_thread = DownloadCheckThread(self.download_queue)
        self.download_check_thread.info_index.connect(self.download_success)
        self.download_check_thread.complete.connect(self.end_download)

        layout.addWidget(self.crawl_display_table)
        self.setLayout(layout)
        self.setStyleSheet("""border: none;margin:0;""")

    @Slot(dict)
    def start_crawl(self, user):
        self.crawl_button.setEnabled(False)
        self.crawl_button.setText("获取中...")
        self.user_id_edit.setEnabled(False)
        user_id = self.user_id_edit.text().strip()
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["ID", "标题", "内容", "点赞数", "评论数", "收藏数", "状态"])
        self.user_note_thread.user_id = user_id
        self.user_note_thread.start()
        self.download_thread.start()
        self.download_check_thread.start()

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
        self.crawl_button.setText("下载中...")

    @Slot(str)
    def show_error(self, msg):
        self.end_download()
        show_error(msg)

    @Slot()
    def end_download(self):
        self.crawl_button.setEnabled(True)
        self.crawl_button.setText("开始")
        self.user_id_edit.setEnabled(True)

    @Slot(dict)
    def success_get_note(self, note):
        self.note_info.append(note)
        self.user_save_path = os.path.join(download_path, note["user_name"])
        add_row_to_table(self.model, self.props, note)

    @Slot(dict)
    def download_success(self, info_dict):
        index = info_dict["index"]
        info = info_dict["info"]
        if info:
            self.model.item(index, len(self.props) - 1).setText(info)

    @Slot(int)
    def download_error(self, index):
        self.model.item(index, len(self.props) - 1).setText("下载出错")

    @Slot()
    def open_download_path(self):
        subprocess.Popen(rf'explorer /select,{self.user_save_path}')


class CrawlNote(QFrame):
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
        open_download_path_button = Button("打开下载文件夹")
        open_download_path_button.clicked.connect(self.open_download_path)
        open_download_path_button.setFixedWidth(150)
        self.crawl_button.clicked.connect(self.start_crawl)
        crawl_config_layout.addWidget(self.note_id_edit)
        crawl_config_layout.addWidget(self.crawl_button)
        crawl_config_layout.addWidget(open_download_path_button)
        layout.addLayout(crawl_config_layout)

        self.crawl_display_table = QTableView()
        self.note_info = []
        init_table(self.crawl_display_table)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            ["ID", "博主", "博主ID", "标题", "内容", "点赞数", "评论数", "收藏数", "状态"])
        self.props = ["note_id", "user_name", "user_id", "title", "desc", "liked_count", "comment_count",
                      "collected_count", "status"]
        self.crawl_display_table.setModel(self.model)
        self.user_save_path = download_path

        self.note_queue = queue.Queue()
        self.download_queue = queue.Queue()

        self.note_thread = GetNoteThread(self.note_queue)
        self.note_thread.note.connect(self.success_get_note)
        self.note_thread.error.connect(self.show_error)

        self.download_thread = NoteDownloadThread(self.note_queue, self.download_queue)
        self.download_thread.complete.connect(self.end_crawl)

        self.download_check_thread = DownloadCheckThread(self.download_queue)
        self.download_check_thread.info_index.connect(self.download_success)
        self.download_check_thread.complete.connect(self.end_download)

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
            self.download_check_thread.start()

    @Slot()
    def end_crawl(self):
        self.crawl_button.setText("下载中...")

    @Slot(str)
    def show_error(self, msg):
        self.end_download()
        show_error(msg)

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

    @Slot(dict)
    def download_success(self, info_dict):
        index = info_dict["index"]
        info = info_dict["info"]
        if info:
            self.model.item(index, len(self.props) - 1).setText(info)

    @Slot(int)
    def download_error(self, index):
        self.model.item(index, len(self.props) - 1).setText("下载出错")

    @Slot()
    def open_download_path(self):
        subprocess.Popen(rf'explorer {self.user_save_path}')
