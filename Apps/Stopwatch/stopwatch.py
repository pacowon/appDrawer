import os, sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, QElapsedTimer
from PyQt5.uic import loadUi

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class StopwatchApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'stopwatch.ui'), self)
        self._elapsed = QElapsedTimer()
        self._offset = 0
        self._running = False
        self._timer = QTimer(self)
        self._timer.setInterval(10)
        self._timer.timeout.connect(self._tick)
        self.btn_start.clicked.connect(self._start)
        self.btn_stop.clicked.connect(self._stop)
        self.btn_reset.clicked.connect(self._reset)
        self.setup_count()

    def _start(self):
        if not self._running:
            self._elapsed.start()
            self._timer.start()
            self._running = True

    def _stop(self):
        if self._running:
            self._offset += self._elapsed.elapsed()
            self._timer.stop()
            self._running = False

    def _reset(self):
        self._timer.stop()
        self._running = False
        self._offset = 0
        self.sw_display.setText("00:00.000")

    def _tick(self):
        ms = self._offset + self._elapsed.elapsed()
        minutes = ms // 60000
        seconds = (ms % 60000) // 1000
        millis = ms % 1000
        self.sw_display.setText(f"{minutes:02d}:{seconds:02d}.{millis:03d}")
