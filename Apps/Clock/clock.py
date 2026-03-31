import os, sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.uic import loadUi

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class ClockApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'clock.ui'), self)
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)
        self._timer.start()
        self._tick()
        self.setup_count()

    def _tick(self):
        now = QDateTime.currentDateTime()
        self.time_label.setText(now.toString("HH:mm:ss"))
        self.date_label.setText(now.toString("yyyy년 MM월 dd일 (ddd)"))
