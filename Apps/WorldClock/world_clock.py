import os, sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QDateTime, QTimeZone
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin
from PyQt5.QtWidgets import QHBoxLayout, QPushButton

ZONES = [
    ("서울",    b"Asia/Seoul"),
    ("도쿄",    b"Asia/Tokyo"),
    ("뉴욕",    b"America/New_York"),
    ("런던",    b"Europe/London"),
    ("파리",    b"Europe/Paris"),
    ("시드니",  b"Australia/Sydney"),
]

class WorldClockApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("세계 시계", alignment=Qt.AlignCenter))
        self.labels = {}
        for city, tz in ZONES:
            row = QHBoxLayout()
            city_lbl = QLabel(city); city_lbl.setFixedWidth(60)
            city_lbl.setFont(QFont("Arial", 12, QFont.Bold))
            time_lbl = QLabel("--:--:--")
            time_lbl.setFont(QFont("Consolas", 14))
            self.labels[tz] = time_lbl
            row.addWidget(city_lbl); row.addWidget(time_lbl); row.addStretch()
            layout.addLayout(row)
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addLayout(cr)
        timer = QTimer(self); timer.setInterval(1000); timer.timeout.connect(self._tick); timer.start()
        self._tick()
        self.setup_count()

    def _tick(self):
        for tz_bytes, lbl in self.labels.items():
            tz = QTimeZone(tz_bytes)
            t = QDateTime.currentDateTime().toTimeZone(tz)
            lbl.setText(t.toString("HH:mm:ss  (yyyy-MM-dd)"))
