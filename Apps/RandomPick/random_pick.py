import os, sys, random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class RandomPickApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("항목 추가 후 랜덤 선택", alignment=Qt.AlignCenter))
        row = QHBoxLayout()
        self.inp = QLineEdit(); self.inp.setPlaceholderText("항목 입력...")
        add_btn = QPushButton("추가"); add_btn.clicked.connect(self._add)
        row.addWidget(self.inp); row.addWidget(add_btn)
        self.lst = QListWidget()
        self.result = QLabel("-", alignment=Qt.AlignCenter)
        self.result.setFont(QFont("Arial", 20, QFont.Bold))
        self.result.setStyleSheet("color:#e74c3c;")
        pick_btn = QPushButton("랜덤 선택!")
        pick_btn.setFixedHeight(44)
        pick_btn.setStyleSheet("font-size:15px;background:#e74c3c;color:white;border:none;border-radius:8px;")
        pick_btn.clicked.connect(self._pick)
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addLayout(row); layout.addWidget(self.lst); layout.addWidget(self.result); layout.addWidget(pick_btn); layout.addLayout(cr)
        self.setup_count()

    def _add(self):
        t = self.inp.text().strip()
        if t: self.lst.addItem(t); self.inp.clear()

    def _pick(self):
        items = [self.lst.item(i).text() for i in range(self.lst.count())]
        if items: self.result.setText(random.choice(items))
