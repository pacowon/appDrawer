import os, sys, random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

CHOICES = {"가위": "✂️", "바위": "✊", "보": "🖐️"}
WIN = {("가위","보"),("바위","가위"),("보","바위")}

class RockPaperScissorsApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        self._score = [0, 0]
        layout = QVBoxLayout(self); layout.setAlignment(Qt.AlignCenter)
        self.score_lbl = QLabel("나 0 : 0 컴퓨터", alignment=Qt.AlignCenter)
        self.score_lbl.setFont(QFont("Arial", 14, QFont.Bold))
        self.result = QLabel("선택하세요!", alignment=Qt.AlignCenter)
        self.result.setFont(QFont("Arial", 18)); self.result.setStyleSheet("padding:10px;")
        row = QHBoxLayout()
        for name, emoji in CHOICES.items():
            btn = QPushButton(f"{emoji}\n{name}"); btn.setFixedSize(90, 80)
            btn.setStyleSheet("font-size:14px;background:#ecf0f1;border:2px solid #bdc3c7;border-radius:10px;")
            btn.clicked.connect(lambda _, n=name: self._play(n))
            row.addWidget(btn)
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(self.score_lbl); layout.addWidget(self.result); layout.addLayout(row); layout.addLayout(cr)
        self.setup_count()

    def _play(self, user):
        comp = random.choice(list(CHOICES.keys()))
        if user == comp: msg = f"무승부! {CHOICES[user]} vs {CHOICES[comp]}"
        elif (user, comp) in WIN: self._score[0] += 1; msg = f"승리! {CHOICES[user]} vs {CHOICES[comp]}"
        else: self._score[1] += 1; msg = f"패배! {CHOICES[user]} vs {CHOICES[comp]}"
        self.result.setText(msg)
        self.score_lbl.setText(f"나 {self._score[0]} : {self._score[1]} 컴퓨터")
