"""
하트 아이콘을 코드로 생성해서 QIcon으로 반환.
외부 이미지 파일 불필요.
"""
import math
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QPainterPath, QBrush
from PyQt5.QtCore import Qt


def make_heart_icon(size: int = 64, color: str = "#e74c3c") -> QIcon:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    path = QPainterPath()
    w, h = size, size

    # 하트 곡선 (파라메트릭)
    # 중심을 약간 위로 올려서 시각적으로 균형 맞춤
    points = []
    for i in range(360):
        t = math.radians(i)
        # 하트 방정식
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
        points.append((x, y))

    # 좌표 정규화 → pixmap 크기에 맞게 스케일
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    pad = size * 0.08

    def tx(x):
        return pad + (x - min_x) / (max_x - min_x) * (w - 2 * pad)

    def ty(y):
        return pad + (y - min_y) / (max_y - min_y) * (h - 2 * pad)

    path.moveTo(tx(points[0][0]), ty(points[0][1]))
    for px, py in points[1:]:
        path.lineTo(tx(px), ty(py))
    path.closeSubpath()

    painter.setBrush(QBrush(QColor(color)))
    painter.setPen(Qt.NoPen)
    painter.drawPath(path)
    painter.end()

    return QIcon(pixmap)
