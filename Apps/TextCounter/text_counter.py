import os, sys
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class TextCounterApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'text_counter.ui'), self)
        self.text_input.textChanged.connect(self.update_stats)
        self.setup_count()

    def update_stats(self):
        text = self.text_input.toPlainText()
        chars = len(text)
        words = len(text.split()) if text.strip() else 0
        lines = text.count('\n') + 1 if text else 0
        self.lbl_chars.setText(f"글자: {chars}")
        self.lbl_words.setText(f"단어: {words}")
        self.lbl_lines.setText(f"줄: {lines}")
