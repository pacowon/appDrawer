import os, sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QScrollArea, QFrame, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

BUTTONS = [
    ("Primary",   "#3498db", "#2980b9"),
    ("Success",   "#2ecc71", "#27ae60"),
    ("Danger",    "#e74c3c", "#c0392b"),
    ("Warning",   "#f39c12", "#d68910"),
    ("Purple",    "#9b59b6", "#8e44ad"),
    ("Dark",      "#2c3e50", "#1a252f"),
    ("Teal",      "#1abc9c", "#16a085"),
    ("Pink",      "#e91e63", "#c2185b"),
    ("Orange",    "#ff5722", "#e64a19"),
    ("Indigo",    "#3f51b5", "#303f9f"),
    ("Cyan",      "#00bcd4", "#0097a7"),
    ("Lime",      "#8bc34a", "#689f38"),
]

class ButtonGalleryApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()
        self.setup_count()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 8)
        root.setSpacing(12)

        title = QLabel("✨ Button Gallery")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color:#2c3e50; padding:8px;")
        root.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")
        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(12)
        grid.setContentsMargins(8, 8, 8, 8)

        styles = [
            ("Filled",   lambda bg, hv: f"QPushButton{{background:{bg};color:white;border:none;border-radius:8px;padding:12px 20px;font-size:14px;font-weight:bold;}}QPushButton:hover{{background:{hv};}}"),
            ("Outline",  lambda bg, hv: f"QPushButton{{background:transparent;color:{bg};border:2px solid {bg};border-radius:8px;padding:12px 20px;font-size:14px;font-weight:bold;}}QPushButton:hover{{background:{bg};color:white;}}"),
            ("Rounded",  lambda bg, hv: f"QPushButton{{background:{bg};color:white;border:none;border-radius:20px;padding:12px 20px;font-size:14px;font-weight:bold;}}QPushButton:hover{{background:{hv};}}"),
            ("Shadow",   lambda bg, hv: f"QPushButton{{background:{bg};color:white;border:none;border-radius:6px;padding:12px 20px;font-size:14px;font-weight:bold;border-bottom:4px solid {hv};}}QPushButton:hover{{background:{hv};border-bottom:2px solid {hv};}}"),
        ]

        for col, (style_name, style_fn) in enumerate(styles):
            lbl = QLabel(style_name)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFont(QFont("Arial", 11, QFont.Bold))
            lbl.setStyleSheet("color:#7f8c8d;")
            grid.addWidget(lbl, 0, col)

        for row, (name, bg, hv) in enumerate(BUTTONS, 1):
            for col, (_, style_fn) in enumerate(styles):
                btn = QPushButton(name)
                btn.setMinimumHeight(44)
                btn.setStyleSheet(style_fn(bg, hv))
                btn.clicked.connect(lambda _, n=name, b=bg: self._on_click(n, b))
                grid.addWidget(btn, row, col)

        scroll.setWidget(container)
        root.addWidget(scroll, 1)

        self.status = QLabel("버튼을 클릭해보세요")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("color:#95a5a6; font-size:12px; padding:4px;")
        root.addWidget(self.status)

        # Count 바
        count_row = QHBoxLayout()
        from PyQt5.QtWidgets import QPushButton as QB, QLabel as QL
        self.btn_count = QB("Count")
        self.btn_count.setFixedHeight(36)
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.btn_show_path = QB("📂 경로")
        self.btn_show_path.setFixedHeight(36)
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.count_label = QL("-")
        self.count_label.setStyleSheet("font-size:20px;font-weight:bold;padding:0 12px;color:#9c27b0;")
        count_row.addWidget(self.btn_count)
        count_row.addWidget(self.btn_show_path)
        count_row.addWidget(self.count_label)
        count_row.addStretch()
        root.addLayout(count_row)

    def _on_click(self, name, color):
        self.status.setText(f"클릭: {name}  |  색상: {color}")
        self.status.setStyleSheet(f"color:{color}; font-size:13px; font-weight:bold; padding:4px;")
