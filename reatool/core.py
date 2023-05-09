import json
import logging
import os
import time
from datetime import datetime

from PySide6.QtCore import QThread, Signal
from xhs import XhsClient, IPBlockError
from xhs.help import get_valid_path_name, get_imgs_urls_from_note, get_video_urls_from_note

from aria2.client import Aria2Client
from .setting import xhs_settings, download_path
from .utils import generate_qrcode_base64

xhs_client = XhsClient(xhs_settings.cookie)


class GenerateQrcodeThread(QThread):
    """
    获取验证码的线程
    """
    qrcode = Signal(dict)
    error = Signal(str)

    def run(self) -> None:
        try:
            qr_dict = xhs_client.get_qrcode()
            qr_dict.update({"base64": generate_qrcode_base64(qr_dict["url"])})
            self.qrcode.emit(qr_dict)
        except Exception as e:
            logging.error(e)
            self.error.emit("创建二维码失败，请刷新")


class CheckQrcodeThread(QThread):
    """验证二维码状态线程"""

    check_status = Signal(dict)

    qr_id = ""
    qr_code = ""

    def run(self) -> None:
        while True:
            try:
                res = xhs_client.check_qrcode(qr_id=self.qr_id, code=self.qr_code)
                code_status = res["code_status"]
                logging.debug(res)
                if code_status == 0:
                    res["msg"] = "请扫码..."
                elif code_status == 1:
                    res["msg"] = "扫码成功!"
                elif code_status == 2:
                    res["msg"] = "登录成功!"
                    self.check_status.emit(res)
                    xhs_settings.cookie = xhs_client.cookie
                    break
                self.check_status.emit(res)
                time.sleep(1)
            except Exception as e:
                logging.error(e)
                self.check_status.emit({"msg": "二维码过期，请刷新"})
                break


class GetSelfUserThread(QThread):
    user = Signal(dict)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        try:
            info = xhs_client.get_self_info()
            logging.info(f"获取个人信息成功：{info}")
            self.user.emit(info)
        except Exception as e:
            logging.error(e)
            self.user.emit(None)


class GetUserThread(QThread):
    user = Signal(dict)
    error = Signal(str)
    user_id = ""

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        try:
            info = xhs_client.get_user_info(self.user_id)
            logging.info(f"获取用户信息成功：{info}")
            self.user.emit(info)
        except Exception as e:
            logging.error(e)
            self.error.emit(str(e))


def get_note_by_id(note_id):
    note = xhs_client.get_note_by_id(note_id)
    logging.info(f"获取笔记成功：{note}")
    interact_info = note["interact_info"]
    result = {
        "note_id": note["note_id"],
        "title": note["title"],
        "desc": note["desc"],
        "type": note["type"],
        "user": note["user"],
        "user_id": note["user"]["user_id"],
        "user_name": note["user"]["nickname"],
        "img_urls": get_imgs_urls_from_note(note),
        "video_urls": get_video_urls_from_note(note),
        "tag_list": note["tag_list"],
        "at_user_list": note["at_user_list"],
        "collected_count": interact_info["collected_count"],
        "comment_count": interact_info["comment_count"],
        "liked_count": interact_info["liked_count"],
        "share_count": interact_info["share_count"],
        "time": note["time"],
        "last_update_time": note["last_update_time"],
    }
    return result


class GetNoteThread(QThread):
    note = Signal(dict)
    error = Signal(str)
    note_id = ""

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        try:
            note = get_note_by_id(self.note_id)
            self.queue.put(note)
            self.queue.put(None)
            self.note.emit(note)
        except Exception as e:
            self.error.emit(str(e))
            logging.error(e)


class GetUserNoteThread(QThread):
    user_id = ""
    note = Signal(dict)
    error = Signal(str)
    completed = Signal()

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        has_more = True
        cursor = ""
        while has_more:
            try:
                res = xhs_client.get_user_notes(self.user_id, cursor)
                note_ids = list(map(lambda item: item["note_id"], res["notes"]))
                logging.info(f"当前页笔记数：{len(note_ids)}")
                for note_id in note_ids:
                    try:
                        result = get_note_by_id(note_id)
                        self.queue.put(result)
                        self.note.emit(result)
                    except IPBlockError as e:
                        raise e
                    except Exception as e:
                        if "笔记状态异常" in repr(e):
                            logging.warning(f"【{note_id}】笔记状态异常，已忽略")
                        else:
                            raise
                    else:
                        time.sleep(0.5)
                has_more = res["has_more"]
                cursor = res["cursor"]
            except Exception as e:
                logging.error(e)
                self.error.emit(f"获取博主笔记错误 \n【网络连接异常】 \n 将暂停三分钟后继续爬取...")
                time.sleep(60 * 3)
            while True and has_more:
                waiting_list = Aria2Client.get_waiting_list()
                logging.debug(f"当前等待下载数为：{len(waiting_list)}, 循环等待至其低于 10 后才获取下一页数据")
                if len(waiting_list) <= 5 * 2:
                    break
                else:
                    time.sleep(10)
        logging.info(f"{self.user_id} 博主笔记爬取结束")
        self.completed.emit()


class NoteDownloadThread(QThread):
    complete = Signal()

    def __init__(self, note_queue):
        super().__init__()
        self.note_queue = note_queue

    def run(self) -> None:
        while note := self.note_queue.get():
            note_id = note["note_id"]
            nickname = note["user"]["nickname"]
            created_time = datetime.fromtimestamp(note["time"] / 1000).strftime("%y%m%d")
            title = get_valid_path_name(note["title"])
            title = created_time + "_" + (title + "_" + note_id if title else note_id)

            user_save_path = os.path.join(download_path, nickname)
            new_dir_path = os.path.join(user_save_path, title)

            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)

            img_urls = note["img_urls"]
            if len(img_urls):
                for index, img_urls in enumerate(img_urls):
                    gids = Aria2Client.add_url(img_urls, f"{title}{index}.png", new_dir_path)
                    logging.info(f"添加下载成功, gids:{gids}, urls: {img_urls}")
            video_urls = note["video_urls"]
            if len(video_urls):
                gids = Aria2Client.add_url(video_urls, f"{title}.mp4", new_dir_path)
                logging.info(f"添加下载成功, gids:{gids}, urls: {video_urls}")
            with open(os.path.join(new_dir_path, "data.json"), "w", encoding="utf-8") as f:
                json.dump(note, f, ensure_ascii=False, indent=4)
            with open(os.path.join(new_dir_path, "文案.txt"), "w", encoding="utf-8") as f:
                f.write(note["desc"])
        self.complete.emit()
