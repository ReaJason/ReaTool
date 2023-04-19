import logging
import os

from reatool.core import root_path

logger = logging.getLogger()
log_dir_path = os.path.join(root_path, "log")

if not os.path.exists(log_dir_path):
    os.makedirs(log_dir_path)

log_file_path = os.path.join(log_dir_path, "app.log")

if not os.path.exists(log_file_path):
    pass

# log format
formatter = logging.Formatter('[%(asctime)s][%(levelname)s]'
                              '[%(threadName)7s] - %(message)s',
                              '%Y-%m-%d %H:%M:%S')

# console log handler
console_log_handler = logging.StreamHandler()
console_log_handler.setFormatter(formatter)

# file log handler
file_log_handler = logging.FileHandler(log_file_path)
file_log_handler.setFormatter(formatter)


# ui log handler
class UIHandler(logging.StreamHandler):
    def __init__(self, callback=None):
        super().__init__()
        self._callback = callback

    def emit(self, record):
        if self._callback:
            msg = self.format(record)
            self._callback(str(msg.encode('utf-8')))


def set_ui_logger(callback):
    ui_log_handler = UIHandler(callback)
    ui_log_handler.setFormatter(formatter)
    logger.addHandler(ui_log_handler)


logger.addHandler(console_log_handler)
logger.addHandler(file_log_handler)
logger.setLevel(logging.DEBUG)
