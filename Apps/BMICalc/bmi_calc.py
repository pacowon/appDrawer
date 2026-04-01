import os, sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDoubleSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class BMICalcApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("BMI 계산기", alignment=Qt.AlignCenter))
        for label, attr, mn, mx, val in [("키 (cm)", "height", 100, 250, 170), ("몸무게 (kg)", "weight", 20, 300, 65)]:
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            spin = QDoubleSpinBox(); spin.setRange(mn, mx); spin.setValue(val); spin.setDecimals(1)
            spin.setStyleSheet("font-size:14px; padding:5px;")
            setattr(self, attr, spin)
            row.addWidget(spin)
            layout.addLayout(row)
        btn = QPushButton("계산")
        btn.setFixedHeight(44)
        btn.setStyleSheet("font-size:15px;background:#3498db;color:white;border:none;border-radius:8px;")
        btn.clicked.connect(self._calc)
        self.result = QLabel("-", alignment=Qt.AlignCenter)
        self.result.setFont(QFont("Arial", 22, QFont.Bold))
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(btn); layout.addWidget(self.result); layout.addLayout(cr)
        self.setup_count()

    def _calc(self):
        h = self.height.value() / 100
        w = self.weight.value()
        bmi = w / (h * h)
        cat = "저체중" if bmi < 18.5 else "정상" if bmi < 25 else "과체중" if bmi < 30 else "비만"
        self.result.setText(f"BMI: {bmi:.1f}  ({cat})")
