import os, sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class ColorMixerApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("색상 믹서", alignment=Qt.AlignCenter))
        self.preview = QFrame(); self.preview.setMinimumHeight(80)
        self.preview.setStyleSheet("background:#ffffff;border-radius:8px;border:1px solid #ddd;")
        self.hex_lbl = QLabel("#FFFFFF", alignment=Qt.AlignCenter)
        self.hex_lbl.setFont(QFont("Consolas", 16, QFont.Bold))
        self.sliders = {}
        for ch, color in [("R","#e74c3c"),("G","#2ecc71"),("B","#3498db")]:
            row = QHBoxLayout()
            lbl = QLabel(ch); lbl.setFixedWidth(20)
            lbl.setStyleSheet(f"font-size:14px;font-weight:bold;color:{color};")
            sl = QSlider(Qt.Horizontal); sl.setRange(0,255); sl.setValue(255)
            sl.setStyleSheet(f"QSlider::handle:horizontal{{background:{color};border-radius:6px;width:14px;height:14px;}}")
            val = QLabel("255"); val.setFixedWidth(35); val.setStyleSheet("font-size:13px;")
            sl.valueChanged.connect(lambda v, l=val: l.setText(str(v)))
            sl.valueChanged.connect(self._update)
            self.sliders[ch] = sl
            row.addWidget(lbl); row.addWidget(sl); row.addWidget(val)
            layout.addLayout(row)
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(self.preview); layout.addWidget(self.hex_lbl); layout.addLayout(cr)
        self._update()
        self.setup_count()

    def _update(self):
        r,g,b = self.sliders["R"].value(), self.sliders["G"].value(), self.sliders["B"].value()
        hex_c = f"#{r:02X}{g:02X}{b:02X}"
        self.preview.setStyleSheet(f"background:{hex_c};border-radius:8px;border:1px solid #ddd;")
        self.hex_lbl.setText(hex_c)
