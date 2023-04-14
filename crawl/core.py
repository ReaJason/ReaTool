import base64
import io
import time

from PySide6.QtCore import QThread, Signal
from xhs import XhsClient
import segno
from .setting_manager import xiaohongshu_set_cookie, xiaohongshu_get_cookie

cookie = xiaohongshu_get_cookie() or "webId=1"
xhs_client = XhsClient(cookie)


def get_qrcode_base64(text):
    qrcode = segno.make(text)
    out = io.BytesIO()
    qrcode.save(out, kind='png', light=None, scale=3)
    return base64.b64encode(out.getvalue()).decode("utf-8")


class GenerateQrcodeThread(QThread):
    """
    获取验证码的线程
    """
    qrcode = Signal(dict)

    def run(self) -> None:
        qr_dict = xhs_client.get_qrcode()
        qr_dict.update({"base64": get_qrcode_base64(qr_dict["url"])})
        self.qrcode.emit(qr_dict)


class CheckQrcodeThread(QThread):
    """验证二维码状态线程"""

    check_status = Signal(dict)

    qr_id = ""
    qr_code = ""

    def run(self) -> None:
        while True:
            res = xhs_client.check_qrcode(qr_id=self.qr_id, code=self.qr_code)
            code_status = res["code_status"]
            print(res)
            if code_status == 0:
                res["msg"] = "请扫码..."
            elif code_status == 1:
                res["msg"] = "扫码成功!"
            elif code_status == 2:
                res["msg"] = "登录成功!"
                self.check_status.emit(res)
                print(xhs_client.cookie)
                xiaohongshu_set_cookie(xhs_client.cookie)
                break
            elif code_status == 3:
                res["msg"] = "二维码过期，请刷新"
                self.check_status.emit(res)
                break
            else:
                res["msg"] = f"出状况了！{res}"
                self.check_status.emit(res)
                break
            self.check_status.emit(res)
            time.sleep(0.5)


class GetSelfUserThread(QThread):
    user = Signal(dict)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        try:
            self.user.emit(xhs_client.get_self_info())
        except Exception as e:
            print(e)
            self.user.emit(None)
