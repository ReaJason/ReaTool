from xhs import XhsClient
from .setting_manager import settings_manager

xhs_client = XhsClient()


def get_qrcode():
    return xhs_client.get_qrcode()
