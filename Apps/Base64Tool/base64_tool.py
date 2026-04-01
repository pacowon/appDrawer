import os, sys, base64
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class Base64ToolApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Base64 인코더/디코더", alignment=Qt.AlignCenter))
        self.inp = QTextEdit(); self.inp.setPlaceholderText("텍스트 입력...")
        self.inp.setMaximumHeight(100)
        row = QHBoxLayout()
        for label, fn, color in [("인코딩", self._enc, "#3498db"), ("디코딩", self._dec, "#e74c3c")]:
            btn = QPushButton(label); btn.setFixedHeight(40)
            btn.setStyleSheet(f"font-size:14px;background:{color};color:white;border:none;border-radius:6px;")
            btn.clicked.connect(fn); row.addWidget(btn)
        self.out = QTextEdit(); self.out.setReadOnly(True); self.out.setMaximumHeight(100)
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(self.inp); layout.addLayout(row); layout.addWidget(self.out); layout.addLayout(cr)
        self.setup_count()

    def _enc(self):
        self.out.setText(base64.b64encode(self.inp.toPlainText().encode()).decode())
    def _dec(self):
        try: self.out.setText(base64.b64decode(self.inp.toPlainText().encode()).decode())
        except: self.out.setText("디코딩 실패")
