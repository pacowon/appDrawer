"""
PathBar: 앱 서랍 화면 하단에 표시되는 전역 작업 경로 바.
경로 변경 시 앱 실행 경로(os.chdir)에 반영된다.
"""
import os
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QPushButton, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class PathBar(QFrame):
    path_changed = pyqtSignal(str)   # 경로 변경 시 외부에 알림

    def __init__(self, initial_path: str = None, parent=None):
        super().__init__(parent)
        self._path = initial_path or os.getcwd()
        self._setup_ui()

    def _setup_ui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedHeight(36)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(8)

        icon = QLabel("📁")
        icon.setFont(QFont("Arial", 12))

        self.path_label = QLabel(self._path)
        self.path_label.setFont(QFont("Consolas", 10))
        self.path_label.setStyleSheet("color:#2c3e50;")
        self.path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.change_btn = QPushButton("경로 변경")
        self.change_btn.setFixedHeight(24)
        self.change_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                border: none; border-radius: 4px;
                padding: 0 10px; font-size: 11px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.change_btn.clicked.connect(self._change_path)

        layout.addWidget(icon)
        layout.addWidget(self.path_label, 1)
        layout.addWidget(self.change_btn)
        self.apply_theme(
            {
                "path_bg": "#ecf0f1",
                "path_border": "#bdc3c7",
                "path_text": "#2c3e50",
                "path_button_bg": "#3498db",
                "path_button_hover": "#2980b9",
                "path_button_text": "#ffffff",
                "path_button_disabled_bg": "#aab7b8",
                "path_button_disabled_text": "#7f8c8d",
                "path_disabled_bg": "#d5d8dc",
                "path_disabled_border": "#aab7b8",
            },
            disabled=False,
        )

    def _change_path(self):
        new_path = QFileDialog.getExistingDirectory(self, "작업 경로 선택", self._path)
        if new_path:
            self.set_path(new_path)

    def set_path(self, path: str):
        self._path = path
        self.path_label.setText(path)
        self.path_changed.emit(path)

    def apply_theme(self, colors, disabled=False):
        bg = colors["path_disabled_bg"] if disabled else colors["path_bg"]
        border = colors["path_disabled_border"] if disabled else colors["path_border"]
        button_bg = colors["path_button_disabled_bg"] if disabled else colors["path_button_bg"]
        button_text = colors["path_button_disabled_text"] if disabled else colors["path_button_text"]
        hover = colors["path_button_disabled_bg"] if disabled else colors["path_button_hover"]

        self.setStyleSheet(f"""
            PathBar {{
                background-color: {bg};
                border-top: 1px solid {border};
            }}
        """)
        self.path_label.setStyleSheet(f"color:{colors['path_text']};")
        self.change_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {button_bg};
                color: {button_text};
                border: none;
                border-radius: 4px;
                padding: 0 10px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
        """)
        self.setEnabled(not disabled)

    @property
    def path(self) -> str:
        return self._path
