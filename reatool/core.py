import asyncio
import base64
import io
import json
import logging
import os
import re
import time

import segno
from PySide6.QtCore import QThread, Signal
from xhs import XhsClient

from aria2.client import Aria2Client
from .setting_manager import xhs_settings

cookie = xhs_settings.cookie or "webId=1"
xhs_client = XhsClient(cookie)
root_path = os.path.abspath(".")
download_path = os.path.join(root_path, "download")
if not os.path.exists(download_path):
    os.makedirs(download_path)


def get_img_url_by_trace_id(trace_id: str):
    return f"https://sns-img-bd.xhscdn.com/{trace_id}?imageView2/format/png"


def _get_img_urls_from_note(note) -> list:
    imgs = note["image_list"]
    if not len(imgs):
        return []
    return [get_img_url_by_trace_id(img["trace_id"]) for img in imgs]


def _get_video_url_from_note(note) -> str:
    if not note.get("video"):
        return ""
    return f"https://sns-video-bd.xhscdn.com/{note['video']['consumer']['origin_video_key']}"


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
            except:
                self.check_status.emit({"msg": "二维码过期，请刷新"})
                break


class GetSelfUserThread(QThread):
    user = Signal(dict)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        try:
            self.user.emit(xhs_client.get_self_info())
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
            self.user.emit(xhs_client.get_user_info(self.user_id))
        except Exception as e:
            logging.error(e)
            self.error.emit(str(e))


def get_note_by_id(note_id):
    note = xhs_client.get_note_by_id(note_id)
    logging.info(note)
    interact_info = note["interact_info"]
    result = {
        "note_id": note["note_id"],
        "title": note["title"],
        "desc": note["desc"],
        "type": note["type"],
        "user": note["user"],
        "user_id": note["user"]["user_id"],
        "user_name": note["user"]["nickname"],
        "img_urls": _get_img_urls_from_note(note),
        "video_url": _get_video_url_from_note(note),
        "tag_list": note["tag_list"],
        "at_user_list": note["at_user_list"],
        "collected_count": interact_info["collected_count"],
        "comment_count": interact_info["comment_count"],
        "liked_count": interact_info["liked_count"],
        "share_count": interact_info["share_count"],
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

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        has_more = True
        cursor = ""
        while has_more:
            res = xhs_client.get_user_notes(self.user_id, cursor)
            time.sleep(5)
            has_more = res["has_more"]
            cursor = res["cursor"]
            note_ids = map(lambda item: item["note_id"], res["notes"])

            for note_id in note_ids:
                result = get_note_by_id(note_id)
                self.queue.put(result)
                self.note.emit(result)
                time.sleep(0.5)
        self.queue.put(None)


class NoteDownloadThread(QThread):
    complete = Signal()

    def __init__(self, note_queue, download_queue):
        super().__init__()
        self.note_queue = note_queue
        self.download_queue = download_queue
        self.index = 0

    def run(self) -> None:
        self.index = 0
        while note := self.note_queue.get():
            title = note["title"]
            desc = note["desc"]
            note_id = note["note_id"]
            model_index = self.index
            self.index += 1
            nickname = note["user"]["nickname"]

            invalid_chars = '<>:"/\\|?*'
            title = re.sub('[{}]'.format(re.escape(invalid_chars)), '_', title)
            if not title:
                title = desc

            user_save_path = os.path.join(download_path, nickname)
            new_dir_path = os.path.join(user_save_path, title + "_" + note_id)

            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)

            img_urls = note["img_urls"]
            gids = []
            if len(img_urls):
                for index, img_url in enumerate(img_urls):
                    gid = Aria2Client.add_url([img_url], f"{title}{index}.png", new_dir_path)
                    gids.append(gid)
            video_url = note["video_url"]
            if video_url:
                gid = Aria2Client.add_url([video_url], f"{title}.mp4", new_dir_path)
                gids.append(gid)

            self.download_queue.put({
                "index": model_index,
                "gids": gids
            })

            with open(os.path.join(new_dir_path, "data.json"), "w", encoding="utf-8") as f:
                json.dump(note, f, ensure_ascii=False, indent=4)
        self.download_queue.put(None)
        self.complete.emit()


class DownloadCheckThread(QThread):
    info_index = Signal(dict)
    complete = Signal()

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        while download := self.queue.get():
            index = download["index"]
            gids = download["gids"]
            done = [0] * len(gids)
            logging.info(f"正在检测第 {index} 个下载状态")
            while True:
                for i, gid in enumerate(gids):
                    res = Aria2Client.check_status(gid)
                    status = res["status"]
                    logging.info(res)
                    if status == "complete":
                        done[i] = 1
                        done_info = ""
                    elif status == "active":
                        done_info = f"下载中, {round(int(res['downloadSpeed']) / 1000000, 2)} M/s"
                    elif status == "error":
                        done_info = "下载出错"
                    elif status == "waiting":
                        done_info = ""
                    else:
                        done_info = "一定是发生什么事情了"
                    self.info_index.emit({"index": index, "info": done_info})

                if sum(done) == len(gids):
                    self.info_index.emit({"index": index, "info": "下载完成"})
                    break
                time.sleep(0.5)
        self.complete.emit()
