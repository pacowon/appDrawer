import os, sys, random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

QUOTES = [
    ("행동이 항상 행복을 가져다주지는 않지만,\n행동 없이는 행복도 없다.", "벤자민 디즈레일리"),
    ("천 리 길도 한 걸음부터.", "노자"),
    ("성공은 열정을 잃지 않고 실패에서 실패로\n걸어가는 능력이다.", "윈스턴 처칠"),
    ("당신이 할 수 있다고 생각하든,\n할 수 없다고 생각하든, 당신이 옳다.", "헨리 포드"),
    ("인생은 자전거 타기와 같다.\n균형을 잡으려면 계속 움직여야 한다.", "알베르트 아인슈타인"),
    ("오늘 할 수 있는 일을 내일로 미루지 마라.", "벤자민 프랭클린"),
    ("실패는 성공의 어머니다.", "토마스 에디슨"),
    ("꿈을 꾸는 사람은 결코 늙지 않는다.", "아나톨 프랑스"),
]

class QuoteOfDayApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self); layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(QLabel("오늘의 명언", alignment=Qt.AlignCenter))
        self.quote_lbl = QLabel("", alignment=Qt.AlignCenter)
        self.quote_lbl.setFont(QFont("Arial", 14))
        self.quote_lbl.setWordWrap(True)
        self.quote_lbl.setStyleSheet("color:#2c3e50;padding:20px;line-height:1.6;")
        self.author_lbl = QLabel("", alignment=Qt.AlignCenter)
        self.author_lbl.setFont(QFont("Arial", 12, QFont.Bold))
        self.author_lbl.setStyleSheet("color:#7f8c8d;padding:5px;")
        btn = QPushButton("새 명언")
        btn.setFixedHeight(44)
        btn.setStyleSheet("font-size:15px;background:#8e44ad;color:white;border:none;border-radius:8px;")
        btn.clicked.connect(self._new_quote)
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(self.quote_lbl); layout.addWidget(self.author_lbl); layout.addWidget(btn); layout.addLayout(cr)
        self._new_quote()
        self.setup_count()

    def _new_quote(self):
        q, a = random.choice(QUOTES)
        self.quote_lbl.setText(f'"{q}"')
        self.author_lbl.setText(f"— {a}")
