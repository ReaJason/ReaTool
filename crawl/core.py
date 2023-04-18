import base64
import concurrent.futures
import io
import json
import os
import re
import time

import asyncio
from PySide6.QtCore import QThread, Signal
from xhs import XhsClient
import segno
from aria2.client import Aria2Client

from .setting_manager import xiaohongshu_set_cookie, xiaohongshu_get_cookie

cookie = xiaohongshu_get_cookie() or "webId=1"
xhs_client = XhsClient(cookie)


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
            print(e)
            self.user.emit(None)


class GetUserThread(QThread):
    user = Signal(dict)
    user_id = ""

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        self.user.emit(xhs_client.get_user_info(self.user_id))


class GetNoteThread(QThread):
    note = Signal(dict)

    def __init__(self, note_id):
        super().__init__()
        self.note_id = note_id

    def run(self) -> None:
        self.note.emit(xhs_client.get_note_by_id(self.note_id))


class GetUserNoteThread(QThread):
    user_id = ""
    note = Signal(dict)

    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.index = 0

    def run(self) -> None:
        self.index = 0
        has_more = True
        cursor = ""
        while has_more:
            res = xhs_client.get_user_notes(self.user_id, cursor)
            has_more = res["has_more"]
            cursor = res["cursor"]
            note_ids = map(lambda item: item["note_id"], res["notes"])

            for note_id in note_ids:
                cur_note = xhs_client.get_note_by_id(note_id)
                print(cur_note)
                interact_info = cur_note["interact_info"]
                result = {
                    "note_id": cur_note["note_id"],
                    "title": cur_note["title"],
                    "desc": cur_note["desc"],
                    "type": cur_note["type"],
                    "user": cur_note["user"],
                    "img_urls": _get_img_urls_from_note(cur_note),
                    "video_url": _get_video_url_from_note(cur_note),
                    "tag_list": cur_note["tag_list"],
                    "at_user_list": cur_note["at_user_list"],
                    "collected_count": interact_info["collected_count"],
                    "comment_count": interact_info["comment_count"],
                    "liked_count": interact_info["liked_count"],
                    "share_count": interact_info["share_count"],
                    "index": self.index
                }
                self.index += 1
                self.queue.put(result)
                self.note.emit(result)
        self.queue.put(None)


class NoteDownloadThread(QThread):
    info_index = Signal(dict)
    complete = Signal()
    error_index = Signal(int)

    def __init__(self, queue, base_path, max_workers):
        super().__init__()
        self.note_queue = queue
        self.base_path = base_path
        self.max_workers = max_workers

    async def run_task(self):
        running_tasks = []
        while note := self.note_queue.get():
            title = note["title"]
            desc = note["desc"]
            note_id = note["note_id"]
            model_index = note["index"]

            invalid_chars = '<>:"/\\|?*'
            title = re.sub('[{}]'.format(re.escape(invalid_chars)), '_', title)
            if not title:
                title = desc

            new_dir_path = os.path.join(self.base_path, title + "_" + note_id)

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

            task = asyncio.create_task(self.check_status(model_index, gids))
            running_tasks.append(task)

            with open(os.path.join(new_dir_path, "data.json"), "w", encoding="utf-8") as f:
                json.dump(note, f, ensure_ascii=False, indent=4)
        await asyncio.gather(*running_tasks)
        self.complete.emit()

    def run(self) -> None:
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_task())
        loop.close()

    async def check_status(self, index, gids):
        while True:
            done = [0] * len(gids)
            for i, gid in enumerate(gids):
                await asyncio.sleep(1)
                res = Aria2Client.check_status(gid)
                print(res)
                """
                active for currently downloading/seeding downloads.
                 waiting for downloads in the queue; download is not started.
                  paused for paused downloads.
                 error for downloads that were stopped because of error.
                  complete for stopped and completed downloads.
                   removed for the downloads removed by user.
                """
                status = res["status"]
                if status == "complete":
                    done[i] = 1
                    done_info = ""
                elif status == "active":
                    done_info = f"下载中, {round(int(res['downloadSpeed']) / 1000000, 2)} M/s"
                elif status == "error":
                    done_info = "下载出错"
                elif status == "waiting":
                    done_info = "等待下载中"
                else:
                    done_info = "一定是发生什么事情了"
                self.info_index.emit({"index": index, "info": done_info})

            if sum(done) == len(gids):
                self.info_index.emit({"index": index, "info": "下载完成"})
                break
