import os, sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDoubleSpinBox, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

RATES = {"KRW":1, "USD":1350, "EUR":1480, "JPY":9.2, "GBP":1720, "CNY":186}

class CurrencyCalcApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("환율 계산기 (고정 환율)", alignment=Qt.AlignCenter))
        row1 = QHBoxLayout()
        self.amount = QDoubleSpinBox(); self.amount.setRange(0, 999999999); self.amount.setValue(1000)
        self.amount.setStyleSheet("font-size:14px;padding:5px;")
        self.from_cur = QComboBox(); self.from_cur.addItems(list(RATES.keys()))
        self.from_cur.setStyleSheet("font-size:14px;padding:5px;")
        row1.addWidget(self.amount); row1.addWidget(self.from_cur)
        row2 = QHBoxLayout()
        self.to_cur = QComboBox(); self.to_cur.addItems(list(RATES.keys())); self.to_cur.setCurrentIndex(1)
        self.to_cur.setStyleSheet("font-size:14px;padding:5px;")
        btn = QPushButton("변환"); btn.setFixedHeight(40)
        btn.setStyleSheet("font-size:14px;background:#27ae60;color:white;border:none;border-radius:6px;")
        btn.clicked.connect(self._convert)
        row2.addWidget(self.to_cur); row2.addWidget(btn)
        self.result = QLabel("-", alignment=Qt.AlignCenter)
        self.result.setFont(QFont("Arial", 20, QFont.Bold))
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addLayout(row1); layout.addLayout(row2); layout.addWidget(self.result); layout.addLayout(cr)
        self.setup_count()

    def _convert(self):
        amt = self.amount.value()
        krw = amt * RATES[self.from_cur.currentText()]
        result = krw / RATES[self.to_cur.currentText()]
        self.result.setText(f"{amt:,.2f} {self.from_cur.currentText()} = {result:,.2f} {self.to_cur.currentText()}")
