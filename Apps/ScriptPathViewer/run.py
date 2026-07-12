# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Script Path Viewer")
    window.resize(520, 260)

    layout = QVBoxLayout(window)
    layout.setContentsMargins(18, 18, 18, 18)
    layout.setSpacing(14)

    title = QLabel("Script Path Viewer", alignment=Qt.AlignCenter)
    title.setStyleSheet("font-size: 24px; font-weight: bold;")

    info = QLabel(
        "This example shows the working directory passed to run.py.",
        alignment=Qt.AlignCenter,
    )
    info.setWordWrap(True)

    path_label = QLabel(os.getcwd())
    path_label.setWordWrap(True)
    path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
    path_label.setStyleSheet("font-size: 14px; padding: 10px;")

    refresh_btn = QPushButton("Refresh Current Path")
    refresh_btn.clicked.connect(lambda: path_label.setText(os.getcwd()))

    layout.addWidget(title)
    layout.addWidget(info)
    layout.addWidget(path_label, 1)
    layout.addWidget(refresh_btn)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
