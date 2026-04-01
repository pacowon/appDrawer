import os, sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

TABLE = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.'}

class MorseApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("모스 부호 변환기", alignment=Qt.AlignCenter))
        self.inp = QLineEdit(); self.inp.setPlaceholderText("텍스트 입력...")
        self.inp.setStyleSheet("font-size:14px;padding:8px;")
        btn = QPushButton("변환")
        btn.setFixedHeight(40)
        btn.setStyleSheet("font-size:14px;background:#e74c3c;color:white;border:none;border-radius:6px;")
        btn.clicked.connect(self._convert)
        self.out = QTextEdit(); self.out.setReadOnly(True)
        self.out.setStyleSheet("font-size:14px;padding:8px;letter-spacing:2px;")
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(self.inp); layout.addWidget(btn); layout.addWidget(self.out); layout.addLayout(cr)
        self.setup_count()

    def _convert(self):
        result = " ".join(TABLE.get(c.upper(), "?") for c in self.inp.text() if c != " ")
        self.out.setText(result)
