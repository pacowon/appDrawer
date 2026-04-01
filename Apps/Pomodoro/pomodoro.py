import os, sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class PomodoroApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        self._secs = 25 * 60; self._running = False
        layout = QVBoxLayout(self); layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(QLabel("🍅 포모도로 타이머", alignment=Qt.AlignCenter))
        self.display = QLabel(self._fmt(), alignment=Qt.AlignCenter)
        self.display.setFont(QFont("Arial", 52, QFont.Bold))
        self.display.setStyleSheet("color:#e74c3c;")
        row = QHBoxLayout()
        self.start_btn = QPushButton("시작")
        self.start_btn.setFixedHeight(44)
        self.start_btn.setStyleSheet("font-size:15px;background:#e74c3c;color:white;border:none;border-radius:8px;")
        self.start_btn.clicked.connect(self._toggle)
        reset_btn = QPushButton("리셋")
        reset_btn.setFixedHeight(44)
        reset_btn.setStyleSheet("font-size:15px;background:#95a5a6;color:white;border:none;border-radius:8px;")
        reset_btn.clicked.connect(self._reset)
        row.addWidget(self.start_btn); row.addWidget(reset_btn)
        self._timer = QTimer(self); self._timer.setInterval(1000); self._timer.timeout.connect(self._tick)
        self.btn_count = QPushButton("Count")
        self.btn_show_path = QPushButton("📂 경로")
        self.btn_show_path.setStyleSheet("font-size:13px;background:#27ae60;color:white;border:none;border-radius:5px;padding:0 12px;")
        self.btn_count.setStyleSheet("font-size:13px;background:#9c27b0;color:white;border:none;border-radius:5px;padding:0 14px;")
        self.count_label = QLabel("-"); self.count_label.setStyleSheet("font-size:18px;font-weight:bold;color:#9c27b0;padding:0 10px;")
        cr = QHBoxLayout(); cr.addWidget(self.btn_count); cr.addWidget(self.btn_show_path); cr.addWidget(self.count_label); cr.addStretch()
        layout.addWidget(self.display); layout.addLayout(row); layout.addLayout(cr)
        self.setup_count()

    def _fmt(self): return f"{self._secs//60:02d}:{self._secs%60:02d}"
    def _toggle(self):
        self._running = not self._running
        self._timer.start() if self._running else self._timer.stop()
        self.start_btn.setText("일시정지" if self._running else "시작")
    def _reset(self): self._timer.stop(); self._running = False; self._secs = 25*60; self.display.setText(self._fmt()); self.start_btn.setText("시작")
    def _tick(self):
        if self._secs > 0: self._secs -= 1; self.display.setText(self._fmt())
        else: self._timer.stop(); self._running = False; self.display.setText("완료! 🎉")
