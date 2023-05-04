import subprocess
import logging

from PySide6.QtWidgets import QMessageBox


def open_directory(dir_path):
    command = rf'explorer "{dir_path}"'
    logging.info(f"当前打开文件路径：{dir_path}，命令为：{command}")
    subprocess.run(command, shell=True)


def show_error_message(msg):
    QMessageBox.critical(None, '错误', msg, QMessageBox.StandardButton.Close)
