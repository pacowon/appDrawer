import os, sys
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

UNITS = {
    "길이 (m 기준)": {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001, "inch": 0.0254, "ft": 0.3048, "mile": 1609.34},
    "무게 (kg 기준)": {"kg": 1, "g": 0.001, "mg": 0.000001, "lb": 0.453592, "oz": 0.0283495},
    "온도":          {"°C": None, "°F": None, "K": None},
}

def convert_temp(value, from_u, to_u):
    if from_u == to_u: return value
    to_c = {"°C": value, "°F": (value - 32) * 5/9, "K": value - 273.15}
    c = to_c[from_u]
    from_c = {"°C": c, "°F": c * 9/5 + 32, "K": c + 273.15}
    return from_c[to_u]

class UnitConverterApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'unit_converter.ui'), self)
        self.combo_type.addItems(list(UNITS.keys()))
        self.combo_type.currentTextChanged.connect(self._load_units)
        self._load_units(self.combo_type.currentText())
        self.spin_input.valueChanged.connect(self._convert)
        self.combo_from.currentTextChanged.connect(self._convert)
        self.combo_to.currentTextChanged.connect(self._convert)
        self.setup_count()

    def _load_units(self, type_name):
        units = list(UNITS[type_name].keys())
        self.combo_from.blockSignals(True)
        self.combo_to.blockSignals(True)
        self.combo_from.clear(); self.combo_from.addItems(units)
        self.combo_to.clear();   self.combo_to.addItems(units)
        if len(units) > 1: self.combo_to.setCurrentIndex(1)
        self.combo_from.blockSignals(False)
        self.combo_to.blockSignals(False)
        self._convert()

    def _convert(self):
        type_name = self.combo_type.currentText()
        from_u = self.combo_from.currentText()
        to_u   = self.combo_to.currentText()
        value  = self.spin_input.value()
        try:
            if type_name == "온도":
                result = convert_temp(value, from_u, to_u)
            else:
                factors = UNITS[type_name]
                result = value * factors[from_u] / factors[to_u]
            self.line_output.setText(f"{result:.6g}")
        except Exception:
            self.line_output.setText("오류")
