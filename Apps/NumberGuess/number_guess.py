import os, sys, random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class NumberGuessApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        self._answer = random.randint(1, 100); self._tries = 0
        layout = QVBoxLayout(self); layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(QLabel("1~100 숫자 맞추기", alignment=Qt.AlignCenter))
        self.hint = QLabel("숫자를 입력하세요", alignment=Qt.AlignCenter)
        self.hint.setFont(QFont("Arial", 16)); self.hint.setStyleSheet("color:#2c3e50;padding:10px;")
        row = QHBoxLayout()
        self.spin = QSpinBox(); self.spin.setRange(1, 100); self.spin.setStyleSheet("font-size:18px;padding:5px;")
        btn = QPushButton("확인"); btn.setFixedHeight(44)
        btn.setStyleSheet("font-size:15px;background:#3498db;color:white;border:none;border-radius:8px;")
        btn.clicked.connect(self._guess)
        reset = QPushButton("새 게임"); reset.setFixedHeight(44)
        reset.setStyleSheet("font-size:15px;background:#95a5a6;color:white;border:none;border-radius:8px;")
        reset.clicked.connect(self._reset)
        row.addWidget(self.spin); row.addWidget(btn); row.addWidget(reset)
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(self.hint); layout.addLayout(row); layout.addLayout(cr)
        self.setup_count()

    def _guess(self):
        g = self.spin.value(); self._tries += 1
        if g < self._answer: self.hint.setText(f"더 큰 수! (시도: {self._tries})")
        elif g > self._answer: self.hint.setText(f"더 작은 수! (시도: {self._tries})")
        else: self.hint.setText(f"정답! 🎉 {self._tries}번 만에 맞췄어요!")

    def _reset(self): self._answer = random.randint(1, 100); self._tries = 0; self.hint.setText("숫자를 입력하세요")
