from PySide6.QtCore import QThread, Signal
import requests


def get_sentence():
    try:
        res = requests.get("https://v1.hitokoto.cn/?c=f&encode=text")
        return res.text
    except:
        return ""


class HitokotoThread(QThread):
    text_signal = Signal(str)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        while True:
            self.text_signal.emit(get_sentence())
            self.sleep(10)
