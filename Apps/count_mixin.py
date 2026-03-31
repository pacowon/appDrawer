"""
CountMixin: 서브프로세스로 1~20 카운트를 실행하고
QTimer로 stdout을 폴링해 UI 레이블에 표시.
카운트 완료 시 현재 경로에 <app_name>.txt 로 결과를 저장.
"""
import sys
import os
import subprocess
from PyQt5.QtCore import QTimer


class CountMixin:
    def setup_count(self):
        self._count_proc = None
        self._count_lines = []          # 누적 카운트 값
        self._get_save_path = None      # AppContainer가 주입하는 경로 콜백
        self._count_timer = QTimer(self)
        self._count_timer.setInterval(100)
        self._count_timer.timeout.connect(self._poll_count)
        self.btn_count.clicked.connect(self.start_count)

    # AppContainer가 호출해서 경로 콜백을 등록
    def set_path_provider(self, callback):
        self._get_save_path = callback

    def start_count(self):
        if self._count_proc and self._count_proc.poll() is None:
            return

        worker = os.path.join(os.path.dirname(__file__), 'count_worker.py')
        self._count_proc = subprocess.Popen(
            [sys.executable, worker],
            stdout=subprocess.PIPE,
            text=True
        )
        self._count_lines = []
        self.count_label.setText("0")
        self._count_timer.start()

    def _poll_count(self):
        if self._count_proc is None:
            self._count_timer.stop()
            return

        line = self._count_proc.stdout.readline()
        if line and line.strip():
            self._count_lines.append(line.strip())
            self.count_label.setText(line.strip())

        if self._count_proc.poll() is not None:
            for line in self._count_proc.stdout:
                if line.strip():
                    self._count_lines.append(line.strip())
                    self.count_label.setText(line.strip())
            self._count_timer.stop()
            self._count_proc = None
            self._save_count()

    def _save_count(self):
        if not self._count_lines:
            return

        # 저장 경로: 콜백이 있으면 사용, 없으면 cwd
        save_dir = self._get_save_path() if self._get_save_path else os.getcwd()

        # 파일명: 클래스명에서 'App' 제거 후 소문자 → ex) CalculatorApp → calculator.txt
        class_name = type(self).__name__          # e.g. "CalculatorApp"
        base_name = class_name.replace("App", "").lower()  # e.g. "calculator"
        file_path = os.path.join(save_dir, f"{base_name}.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self._count_lines) + "\n")
