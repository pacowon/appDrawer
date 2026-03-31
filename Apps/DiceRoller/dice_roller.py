import os, sys, random
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

FACES = {6: ["⚀","⚁","⚂","⚃","⚄","⚅"], 12: None, 20: None}

class DiceRollerApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'dice_roller.ui'), self)
        self.btn_d6.clicked.connect(lambda: self.roll(6))
        self.btn_d12.clicked.connect(lambda: self.roll(12))
        self.btn_d20.clicked.connect(lambda: self.roll(20))
        self.setup_count()

    def roll(self, sides):
        result = random.randint(1, sides)
        if sides == 6:
            self.dice_display.setText(FACES[6][result - 1])
        else:
            self.dice_display.setText("🎲")
        self.result_label.setText(str(result))
