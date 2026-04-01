import os, sys, random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

DIRS = ["북 ↑","북동 ↗","동 →","남동 ↘","남 ↓","남서 ↙","서 ←","북서 ↖"]

class CompassApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self); layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(QLabel("나침반 (랜덤)", alignment=Qt.AlignCenter))
        self.arrow = QLabel("?", alignment=Qt.AlignCenter)
        self.arrow.setFont(QFont("Arial", 56, QFont.Bold))
        self.arrow.setStyleSheet("color:#2c3e50;")
        btn = QPushButton("방향 확인")
        btn.setFixedHeight(48)
        btn.setStyleSheet("font-size:16px;background:#2c3e50;color:white;border:none;border-radius:8px;")
        btn.clicked.connect(lambda: self.arrow.setText(random.choice(DIRS)))
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(self.arrow); layout.addWidget(btn); layout.addLayout(cr)
        self.setup_count()
