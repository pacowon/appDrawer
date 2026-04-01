import os, sys, random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class FlipcoinApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.result = QLabel("?")
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setFont(QFont("Arial", 72, QFont.Bold))
        btn = QPushButton("동전 던지기")
        btn.setFixedHeight(50)
        btn.setStyleSheet("font-size:16px;background:#f39c12;color:white;border:none;border-radius:8px;")
        btn.clicked.connect(self._flip)
        from PyQt5.QtWidgets import QHBoxLayout, QLabel as QL
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setFixedHeight(36)
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QL("-")
        self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        row = QHBoxLayout()
        row.addWidget(self.btn_count); row.addWidget(self.count_label); row.addStretch()
        layout.addWidget(self.result)
        layout.addWidget(btn)
        layout.addLayout(row)
        self.setup_count()

    def _flip(self):
        r = random.choice(["앞면 🪙", "뒷면 🌑"])
        self.result.setText(r)
