import os, sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDateEdit
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class AgeCalcApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("나이 계산기", alignment=Qt.AlignCenter))
        row = QHBoxLayout()
        row.addWidget(QLabel("생년월일:"))
        self.date_edit = QDateEdit(QDate(1990, 1, 1))
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet("font-size:14px; padding:5px;")
        row.addWidget(self.date_edit)
        layout.addLayout(row)
        btn = QPushButton("계산")
        btn.setFixedHeight(44)
        btn.setStyleSheet("font-size:15px;background:#9b59b6;color:white;border:none;border-radius:8px;")
        btn.clicked.connect(self._calc)
        self.result = QLabel("-", alignment=Qt.AlignCenter)
        self.result.setFont(QFont("Arial", 20, QFont.Bold))
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(btn); layout.addWidget(self.result); layout.addLayout(cr)
        self.setup_count()

    def _calc(self):
        birth = self.date_edit.date()
        today = QDate.currentDate()
        age = today.year() - birth.year()
        if today < QDate(today.year(), birth.month(), birth.day()):
            age -= 1
        days = birth.daysTo(today)
        self.result.setText(f"만 {age}세  ({days:,}일 살았어요)")
