import os, sys, random, string
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QSpinBox, QCheckBox
from PyQt5.QtCore import Qt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class PasswordGenApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("비밀번호 생성기", alignment=Qt.AlignCenter))
        row = QHBoxLayout()
        row.addWidget(QLabel("길이:"))
        self.length = QSpinBox(); self.length.setRange(4, 64); self.length.setValue(16)
        row.addWidget(self.length)
        layout.addLayout(row)
        self.use_upper = QCheckBox("대문자"); self.use_upper.setChecked(True)
        self.use_digit = QCheckBox("숫자");   self.use_digit.setChecked(True)
        self.use_sym   = QCheckBox("특수문자"); self.use_sym.setChecked(True)
        layout.addWidget(self.use_upper); layout.addWidget(self.use_digit); layout.addWidget(self.use_sym)
        btn = QPushButton("생성")
        btn.setFixedHeight(44)
        btn.setStyleSheet("font-size:15px;background:#1abc9c;color:white;border:none;border-radius:8px;")
        btn.clicked.connect(self._gen)
        self.out = QLineEdit(); self.out.setReadOnly(True)
        self.out.setStyleSheet("font-size:14px;padding:8px;letter-spacing:2px;")
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(btn); layout.addWidget(self.out); layout.addLayout(cr)
        self.setup_count()

    def _gen(self):
        pool = string.ascii_lowercase
        if self.use_upper.isChecked(): pool += string.ascii_uppercase
        if self.use_digit.isChecked(): pool += string.digits
        if self.use_sym.isChecked():   pool += "!@#$%^&*"
        self.out.setText("".join(random.choices(pool, k=self.length.value())))
