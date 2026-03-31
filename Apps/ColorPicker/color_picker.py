import os, sys
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from count_mixin import CountMixin

class ColorPickerApp(CountMixin, QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'color_picker.ui'), self)
        for slider, spin in [(self.slider_r, self.spin_r),
                             (self.slider_g, self.spin_g),
                             (self.slider_b, self.spin_b)]:
            slider.valueChanged.connect(lambda v, s=spin: s.setValue(v))
            spin.valueChanged.connect(lambda v, sl=slider: sl.setValue(v))
            slider.valueChanged.connect(self._update_color)
        self._update_color()
        self.setup_count()

    def _update_color(self):
        r, g, b = self.slider_r.value(), self.slider_g.value(), self.slider_b.value()
        hex_color = f"#{r:02X}{g:02X}{b:02X}"
        self.color_preview.setStyleSheet(f"background-color: {hex_color}; border-radius: 8px;")
        self.hex_label.setText(hex_color)
