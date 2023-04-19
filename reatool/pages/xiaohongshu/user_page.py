import time

from PySide6.QtCore import Qt, Slot, Signal, QSize, QThread
from PySide6.QtGui import QStandardItemModel, QStandardItem, QResizeEvent, QFont
from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QTableView, QTabBar, QTabWidget

from reatool.core import GetSelfUserThread
from reatool.widget import Button, LineEdit, init_table
from .welcome import WelComeCard
from .crawl_notes import CrawlUserNotes, CrawlNote


class UserPage(QWidget):
    fetch_success = Signal(bool)
    logout = Signal(bool)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.get_self_info_thread = GetSelfUserThread()
        self.get_self_info_thread.user.connect(self.get_self_info)

        welcome_layout = QHBoxLayout()
        self.welcome_card = WelComeCard()
        self.welcome_card.logout.connect(self.logout_success)
        self.welcome_card.refresh_user_info.connect(self.get_self_info_thread.start)
        welcome_layout.addWidget(self.welcome_card)

        self.layout.addLayout(welcome_layout)
        self.layout.addSpacing(10)

        tab_bar = QTabWidget()
        tab_bar.addTab(CrawlNote(), "笔记详情")
        tab_bar.addTab(CrawlUserNotes(), "用户笔记")
        # tab_bar.addTab(CrawlComments(), "笔记评论")
        # tab_bar.addTab(CrawlSetting(), "设置")
        tab_bar.addTab(CrawlAbout(), "关于")
        tab_bar.setStyleSheet("""
        QTabWidget::pane {
            border: none;
        }
        
        QTabWidget::tab-bar {
            left: 32px
        }
        
        /* Style the tab using the tab sub-control. Note that
            it reads QTabBar _not_ QTabWidget */
        QTabBar::tab {
            border: none;
            padding: 5px 16px;
            margin: 0 4px;
        }
        
        QTabBar::tab:selected, QTabBar::tab:hover {
        }
        
        QTabBar::tab:selected {
            border-bottom: 2px solid #fd8c73;
        }
        
        QTabBar::tab:!selected {
            border-bottom: 2px solid transparent;
        }
        
        """)
        self.layout.addWidget(tab_bar)

        self.get_self_info_thread.start()
        self.setLayout(self.layout)
        self.setStyleSheet("""

        QFrame {
           background-color: #ffffff;
            border-color: #d0d7de;
            border-radius: 6px;
            border-style: solid;
            border-width: 1px;
            margin: 0 30px;
        }

        QLabel{
            border: none;
            margin: 0;
        }

        QToolTip {
        border: none;
        margin: 0;
        }
        QHeaderView {
            margin: 0
        }

        """)

    @Slot(dict)
    def get_self_info(self, user):
        if not user:
            self.fetch_success.emit(False)
            return
        print(user)
        self.welcome_card.refresh(user)

    @Slot()
    def logout_success(self):
        print("退出登录")
        self.logout.emit(True)

    def resizeEvent(self, event: QResizeEvent) -> None:
        pass


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

    @Slot(dict)
    def add_row_to_table(self, row):
        items = []
        for j, (key, value) in enumerate(row.items()):
            item = QStandardItem(str(value))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setSizeHint(QSize(0, 35))
            font = QFont()
            font.setPixelSize(12)
            item.setFont(font)
            items.append(item)
        self.model.appendRow(items)


class CrawlSetting(QFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setStyleSheet("""border: none;margin:0;""")


class CrawlAbout(QFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_info = QLabel("""
        <center>
            <h3>关于</h3>
            当前爬虫使用的是封装的 Python 小工具 <a href='https://github.com/ReaJason/xhs'>xhs</a> 欢迎 star ✨
            <h3>联系我</h3>
            <ul>
                <li>博客✨：<a href='https://reajason.eu.org'>reajason.eu.org</a></li>
                <li>邮箱📮：<a href='mailto:reajason1225@gmail.com'>reajason1225@gmail.com</a></li>
                <li>GitHub🎉：<a href='https://github.com/ReaJason'>ReaJason</a></li>
            </ul>
            <h3>免责声明</h3>
            <ol>
              <li>本软件采集到的内容均可在网页上获取到，所有内容版权归原作者所有。</li>
              <li>本软件提供的所有资源，仅可用于学习交流使用，未经原作者授权，禁止用于其他用途。</li>
              <li>请在 24 小时内删除你所下载的资源，为尊重作者版权，请前往资源发布网站观看，支持原创</li>
              <li>任何涉及商业盈利目的均不得使用，否则一些后果由您承担</li>
              <li>因使用本软件产生的版权问题，软件作者概不负责</li>
            </ol>
        </center>
        
        """)
        about_info.setOpenExternalLinks(True)
        layout.addWidget(about_info)
        self.setLayout(layout)
        self.setStyleSheet("""border: none;margin:0;""")
