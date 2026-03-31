import os
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin


class NotesApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'notes.ui')
        loadUi(ui_path, self)
        self.setup_count()
