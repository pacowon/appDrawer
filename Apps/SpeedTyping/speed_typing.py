import os, sys, random, time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

WORDS = ["python","keyboard","developer","algorithm","interface","function","variable","database","network","security"]

class SpeedTypingApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        self._start = None; self._word = ""
        layout = QVBoxLayout(self); layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(QLabel("타이핑 속도 테스트", alignment=Qt.AlignCenter))
        self.target = QLabel("-", alignment=Qt.AlignCenter)
        self.target.setFont(QFont("Consolas", 28, QFont.Bold))
        self.target.setStyleSheet("color:#3498db;padding:10px;")
        self.inp = QLineEdit(); self.inp.setStyleSheet("font-size:18px;padding:8px;")
        self.inp.textChanged.connect(self._check)
        self.result = QLabel("", alignment=Qt.AlignCenter)
        self.result.setStyleSheet("font-size:14px;color:#27ae60;")
        btn = QPushButton("시작")
        btn.setFixedHeight(44)
        btn.setStyleSheet("font-size:15px;background:#3498db;color:white;border:none;border-radius:8px;")
        btn.clicked.connect(self._start_game)
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(self.target); layout.addWidget(self.inp); layout.addWidget(self.result); layout.addWidget(btn); layout.addLayout(cr)
        self.setup_count()

    def _start_game(self):
        self._word = random.choice(WORDS); self.target.setText(self._word)
        self.inp.clear(); self.inp.setFocus(); self._start = time.time()

    def _check(self, text):
        if self._start and text == self._word:
            elapsed = time.time() - self._start
            self.result.setText(f"완료! {elapsed:.2f}초 ({len(self._word)/elapsed*60:.0f} CPM)")
            self._start = None
