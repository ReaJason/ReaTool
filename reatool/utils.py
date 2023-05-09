import base64
import io
import subprocess
import webbrowser

import browser_cookie3
import requests
import segno
from PySide6.QtWidgets import QMessageBox


def get_cookie_from_local(domain_name: str = ""):
    cj = browser_cookie3.load(domain_name=domain_name)
    cookie_dict = requests.utils.dict_from_cookiejar(cj)
    return ";".join([f"{key}={value}" for key, value in cookie_dict.items()])


def generate_qrcode_base64(text):
    """ text to qrcode base64, but only contains base64 str

    :param text: qrcode content
    :return: base64 str, not include the header -> "data:image/png;base64,"
    """
    qrcode = segno.make(text)
    out = io.BytesIO()
    qrcode.save(out, kind='png', light=None, scale=3)
    return base64.b64encode(out.getvalue()).decode("utf-8")


def open_url(url):
    """open url in system browser

    :param url: url you want to open
    """
    webbrowser.open_new_tab(url)


def open_directory(dir_path):
    """ open directory in system file manager

    :param dir_path: the directory path you want to open
    """
    windows_command = rf'explorer "{dir_path}"'
    subprocess.run(windows_command, shell=True)


def show_error_message(msg):
    """ show error message dialog

    :param msg: error msg
    """
    QMessageBox.critical(None, '错误', msg, QMessageBox.StandardButton.Close)
