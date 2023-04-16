from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QPainterPath


def get_avatar(avatar, size=80):
    target = QPixmap(size, size)
    target.fill(Qt.transparent)

    painter = QPainter(target)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

    path = QPainterPath()
    path.addRoundedRect(0, 0, size, size, size / 2, size / 2)

    painter.setClipPath(path)
    painter.drawPixmap(0, 0, avatar)
    return target
