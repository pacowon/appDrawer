import os, sys, hashlib
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox
from PyQt5.QtCore import Qt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class HashGenApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("해시 생성기", alignment=Qt.AlignCenter))
        self.inp = QLineEdit(); self.inp.setPlaceholderText("텍스트 입력...")
        self.inp.setStyleSheet("font-size:14px;padding:8px;")
        row = QHBoxLayout()
        self.algo = QComboBox(); self.algo.addItems(["md5","sha1","sha256","sha512"])
        self.algo.setStyleSheet("font-size:14px;padding:5px;")
        btn = QPushButton("생성"); btn.setFixedHeight(40)
        btn.setStyleSheet("font-size:14px;background:#8e44ad;color:white;border:none;border-radius:6px;")
        btn.clicked.connect(self._gen)
        row.addWidget(self.algo); row.addWidget(btn)
        self.out = QLineEdit(); self.out.setReadOnly(True)
        self.out.setStyleSheet("font-size:12px;padding:8px;")
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(self.inp); layout.addLayout(row); layout.addWidget(self.out); layout.addLayout(cr)
        self.setup_count()

    def _gen(self):
        h = hashlib.new(self.algo.currentText(), self.inp.text().encode()).hexdigest()
        self.out.setText(h)
