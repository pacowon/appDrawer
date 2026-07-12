# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget


def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Script Note")
    window.resize(520, 420)

    layout = QVBoxLayout(window)
    layout.setContentsMargins(18, 18, 18, 18)
    layout.setSpacing(12)

    title = QLabel("Script Note", alignment=Qt.AlignCenter)
    title.setStyleSheet("font-size: 24px; font-weight: bold;")

    desc = QLabel(
        "This example app is launched by running its own run.py file.",
        alignment=Qt.AlignCenter,
    )
    desc.setWordWrap(True)

    editor = QTextEdit()
    editor.setPlaceholderText("Write anything here...")

    save_btn = QPushButton("Save To script_note.txt")

    def save_note():
        path = os.path.join(os.getcwd(), "script_note.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(editor.toPlainText())
        desc.setText(f"Saved to: {path}")

    save_btn.clicked.connect(save_note)

    layout.addWidget(title)
    layout.addWidget(desc)
    layout.addWidget(editor, 1)
    layout.addWidget(save_btn)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
