"""
PathBar: 앱 위젯 하단에 현재 경로 표시 + 경로 변경 버튼을 붙여주는 래퍼 위젯.
각 앱 인스턴스는 독립적인 작업 경로를 가진다.
"""
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFileDialog, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class PathBar(QFrame):
    """경로 표시 + 변경 버튼 바"""

    def __init__(self, initial_path: str, parent=None):
        super().__init__(parent)
        self._path = initial_path
        self._setup_ui()

    def _setup_ui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            PathBar {
                background-color: #ecf0f1;
                border-top: 1px solid #bdc3c7;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        icon = QLabel("📁")
        icon.setFont(QFont("Arial", 13))

        self.path_label = QLabel(self._path)
        self.path_label.setFont(QFont("Consolas", 10))
        self.path_label.setStyleSheet("color: #2c3e50;")
        self.path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.path_label.setMinimumWidth(0)
        self.path_label.setSizePolicy(
            self.path_label.sizePolicy().horizontalPolicy(),
            self.path_label.sizePolicy().verticalPolicy()
        )

        self.change_btn = QPushButton("경로 변경")
        self.change_btn.setFixedHeight(28)
        self.change_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 12px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.change_btn.clicked.connect(self._change_path)

        layout.addWidget(icon)
        layout.addWidget(self.path_label, 1)
        layout.addWidget(self.change_btn)

    def _change_path(self):
        new_path = QFileDialog.getExistingDirectory(
            self, "작업 경로 선택", self._path
        )
        if new_path:
            self.set_path(new_path)

    def set_path(self, path: str):
        self._path = path
        self.path_label.setText(path)

    @property
    def path(self) -> str:
        return self._path


class AppContainer(QWidget):
    """앱 위젯 + PathBar를 수직으로 묶는 컨테이너"""

    def __init__(self, app_widget: QWidget, initial_path: str = None):
        super().__init__()
        if initial_path is None:
            initial_path = os.getcwd()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(app_widget, 1)

        self.path_bar = PathBar(initial_path)
        layout.addWidget(self.path_bar)

        # CountMixin을 가진 앱이면 경로 콜백 주입
        if hasattr(app_widget, 'set_path_provider'):
            app_widget.set_path_provider(lambda: self.path_bar.path)

    @property
    def current_path(self) -> str:
        return self.path_bar.path
