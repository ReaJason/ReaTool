import requests
from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QPixmap, QPainter, QPainterPath


def get_circle_image_from_url(url, size=80):
    target = QPixmap(size, size)
    target.fill(Qt.transparent)

    circle = QPixmap()
    circle.loadFromData(QByteArray(requests.get(url).content))

    painter = QPainter(target)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

    path = QPainterPath()
    path.addRoundedRect(0, 0, size, size, size / 2, size / 2)

    painter.setClipPath(path)
    painter.drawPixmap(0, 0, circle.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.SmoothTransformation))
    return target
