import os
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin


class CalculatorApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'calculator.ui')
        loadUi(ui_path, self)

        self.current_value = "0"
        self.previous_value = ""
        self.operation = ""
        self.new_number = True

        self.connect_buttons()
        self.setup_count()

    def connect_buttons(self):
        self.btn_0.clicked.connect(lambda: self.number_clicked("0"))
        self.btn_1.clicked.connect(lambda: self.number_clicked("1"))
        self.btn_2.clicked.connect(lambda: self.number_clicked("2"))
        self.btn_3.clicked.connect(lambda: self.number_clicked("3"))
        self.btn_4.clicked.connect(lambda: self.number_clicked("4"))
        self.btn_5.clicked.connect(lambda: self.number_clicked("5"))
        self.btn_6.clicked.connect(lambda: self.number_clicked("6"))
        self.btn_7.clicked.connect(lambda: self.number_clicked("7"))
        self.btn_8.clicked.connect(lambda: self.number_clicked("8"))
        self.btn_9.clicked.connect(lambda: self.number_clicked("9"))
        self.btn_dot.clicked.connect(self.dot_clicked)
        self.btn_add.clicked.connect(lambda: self.operation_clicked("+"))
        self.btn_subtract.clicked.connect(lambda: self.operation_clicked("-"))
        self.btn_multiply.clicked.connect(lambda: self.operation_clicked("*"))
        self.btn_divide.clicked.connect(lambda: self.operation_clicked("/"))
        self.btn_percent.clicked.connect(self.percent_clicked)
        self.btn_equals.clicked.connect(self.equals_clicked)
        self.btn_clear.clicked.connect(self.clear_clicked)
        self.btn_backspace.clicked.connect(self.backspace_clicked)

    def number_clicked(self, number):
        if self.new_number:
            self.current_value = number
            self.new_number = False
        else:
            self.current_value = number if self.current_value == "0" else self.current_value + number
        self.update_display()

    def dot_clicked(self):
        if "." not in self.current_value:
            if self.new_number:
                self.current_value = "0."
                self.new_number = False
            else:
                self.current_value += "."
            self.update_display()

    def operation_clicked(self, op):
        if self.operation and not self.new_number:
            self.equals_clicked()
        self.previous_value = self.current_value
        self.operation = op
        self.new_number = True

    def equals_clicked(self):
        if not self.operation or not self.previous_value:
            return
        try:
            prev, curr = float(self.previous_value), float(self.current_value)
            ops = {"+": prev + curr, "-": prev - curr, "*": prev * curr}
            if self.operation == "/":
                if curr == 0:
                    self.current_value = "Error"
                    self.update_display()
                    self.clear_clicked()
                    return
                result = prev / curr
            else:
                result = ops[self.operation]
            self.current_value = str(int(result)) if result == int(result) else str(round(result, 8))
            self.operation = ""
            self.previous_value = ""
            self.new_number = True
            self.update_display()
        except Exception:
            self.current_value = "Error"
            self.update_display()
            self.clear_clicked()

    def percent_clicked(self):
        try:
            self.current_value = str(float(self.current_value) / 100)
            self.update_display()
        except Exception:
            pass

    def clear_clicked(self):
        self.current_value = "0"
        self.previous_value = ""
        self.operation = ""
        self.new_number = True
        self.update_display()

    def backspace_clicked(self):
        if len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
        else:
            self.current_value = "0"
            self.new_number = True
        self.update_display()

    def update_display(self):
        self.display.setText(self.current_value)
