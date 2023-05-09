from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout


class CrawlAbout(QFrame):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_info = QLabel("""
        <center>
            <h3>关于</h3>
            当前爬虫使用的是封装的 Python 小工具 <a href='https://github.com/ReaJason/xhs'>xhs</a> 欢迎 star ✨ <br>
            更新地址：<a href='https://lingsiki.lanzouw.com/b0en2jwzg#passwd=cih8'>https://lingsiki.lanzouw.com/b0en2jwzg</a> 密码:cih8
            <h3>联系我</h3>
            <ul>
                <li>博客✨：<a href='https://reajason.eu.org'>reajason.eu.org</a></li>
                <li>邮箱📮：<a href='mailto:reajason1225@gmail.com'>reajason1225@gmail.com</a></li>
                <li>GitHub🎉：<a href='https://github.com/ReaJason'>ReaJason</a></li>
                <li>反馈 Q 群：<a href='https://qm.qq.com/cgi-bin/qm/qr?k=huecmkD_IJakRzgUqAuvD9AuNcZMDD0M&jump_from=webapi&authKey=RmsSlr5gKzu2VKybffEKLex914gFYK7R6BmJZVSGbrf5+ZqG0eIAttkw0+HlMjrQ'>615163958</a></li>
            </ul>
            <h3>Buy me a coffee</h3>
            如果觉得这个小工具有帮到您的话，欢迎打赏一杯奶茶 ☕️ 
        </center>
        """)
        about_info.setOpenExternalLinks(True)
        pay_layout = QHBoxLayout()
        pay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wechat_pay = QLabel()
        wechat_pay.setPixmap(QPixmap("asserts/wechat.png").scaledToWidth(150))
        ali_pay = QLabel()
        ali_pay.setPixmap(QPixmap("asserts/alipay.jpg").scaledToWidth(140))
        pay_layout.addWidget(wechat_pay)
        pay_layout.addWidget(ali_pay)
        layout.addWidget(about_info)
        layout.addLayout(pay_layout)
        layout.addWidget(QLabel("<center><h3>免责声明</h3></center>"))
        layout.addWidget(QLabel("""
            <ol>
              <li>本软件采集到的内容均可在网页上获取到，所有内容版权归原作者所有。</li>
              <li>本软件提供的所有资源，仅可用于学习交流使用，未经原作者授权，禁止用于其他用途。</li>
              <li>请在 24 小时内删除你所下载的资源，为尊重作者版权，请前往资源发布网站观看，支持原创</li>
              <li>任何涉及商业盈利目的均不得使用，否则一些后果由您承担</li>
              <li>因使用本软件产生的版权问题，软件作者概不负责</li>
            </ol>
        """))
        self.setLayout(layout)
        self.setStyleSheet("""border: none;margin:0;""")
