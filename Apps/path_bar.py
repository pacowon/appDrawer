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
        self.setStyleSheet("""
            PathBar {
                background-color: #ecf0f1;
                border-top: 1px solid #bdc3c7;
            }
        """)
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

    def _change_path(self):
        new_path = QFileDialog.getExistingDirectory(self, "작업 경로 선택", self._path)
        if new_path:
            self.set_path(new_path)

    def set_path(self, path: str):
        self._path = path
        self.path_label.setText(path)
        self.path_changed.emit(path)

    @property
    def path(self) -> str:
        return self._path
