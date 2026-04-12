import os, sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class CounterApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        self._n = 0
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.lbl = QLabel("0")
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setFont(QFont("Arial", 80, QFont.Bold))
        self.lbl.setStyleSheet("color:#2c3e50;")
        row = QHBoxLayout()
        for text, color in [("-10","#e74c3c"), ("-1","#e67e22"), ("+1","#2ecc71"), ("+10","#3498db")]:
            d = int(text)
            btn = QPushButton(text)
            btn.setFixedSize(70, 50)
            btn.setStyleSheet(f"font-size:18px;font-weight:bold;background:{color};color:white;border:none;border-radius:8px;")
            btn.clicked.connect(lambda _, v=d: self._change(v))
            row.addWidget(btn)
        reset = QPushButton("Reset")
        reset.setFixedHeight(40)
        reset.setStyleSheet("font-size:14px;background:#95a5a6;color:white;border:none;border-radius:8px;")
        reset.clicked.connect(lambda: self._change(-self._n))
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(self.lbl); layout.addLayout(row); layout.addWidget(reset); layout.addLayout(cr)
        self.setup_count()

    def _change(self, v):
        self._n += v
        self.lbl.setText(str(self._n))
