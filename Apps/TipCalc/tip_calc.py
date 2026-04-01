import os, sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDoubleSpinBox, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class TipCalcApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("팁 계산기", alignment=Qt.AlignCenter))
        for lbl, attr, cls, rng, val in [
            ("금액 (원)", "amount", QDoubleSpinBox, (0, 9999999), 50000),
            ("팁 (%)",    "tip_pct", QSpinBox,       (0, 100),     15),
            ("인원수",    "people",  QSpinBox,        (1, 100),     2),
        ]:
            row = QHBoxLayout(); row.addWidget(QLabel(lbl))
            spin = cls(); spin.setRange(*rng); spin.setValue(val)
            spin.setStyleSheet("font-size:14px;padding:5px;")
            setattr(self, attr, spin); row.addWidget(spin); layout.addLayout(row)
        btn = QPushButton("계산")
        btn.setFixedHeight(44)
        btn.setStyleSheet("font-size:15px;background:#e67e22;color:white;border:none;border-radius:8px;")
        btn.clicked.connect(self._calc)
        self.result = QLabel("-", alignment=Qt.AlignCenter)
        self.result.setFont(QFont("Arial", 16, QFont.Bold))
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(btn); layout.addWidget(self.result); layout.addLayout(cr)
        self.setup_count()

    def _calc(self):
        amt = self.amount.value(); tip = self.tip_pct.value(); ppl = self.people.value()
        total = amt * (1 + tip / 100)
        per = total / ppl
        self.result.setText(f"총액: {total:,.0f}원\n1인당: {per:,.0f}원")
