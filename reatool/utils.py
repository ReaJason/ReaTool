import subprocess
import logging


def open_directory(dir_path):
    command = rf'start {dir_path}\\'
    logging.info(f"当前打开文件路径：{dir_path}，命令为：{command}")
    subprocess.run(command, shell=True)
