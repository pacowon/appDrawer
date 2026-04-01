"""
CountMixin: 서브프로세스로 1~20 카운트를 실행하고
QTimer로 stdout을 폴링해 UI 레이블에 표시.
숫자가 들어올 때마다 즉시 현재 경로에 <appname>.txt 로 저장.
"""
import sys
import os
import subprocess
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox


class CountMixin:
    def setup_count(self):
        self._count_proc  = None
        self._get_save_path = None
        self._count_timer = QTimer(self)
        self._count_timer.setInterval(100)
        self._count_timer.timeout.connect(self._poll_count)
        self.btn_count.clicked.connect(self.start_count)
        # 경로 출력 버튼 연결 (ui에 btn_show_path 가 있으면)
        if hasattr(self, 'btn_show_path'):
            self.btn_show_path.clicked.connect(self._show_path)

    def set_path_provider(self, callback):
        self._get_save_path = callback

    def _show_path(self):
        path = self._get_save_path() if self._get_save_path else os.getcwd()
        QMessageBox.information(self, "현재 경로", path)

    # 저장 파일 경로
    def _file_path(self):
        save_dir = self._get_save_path() if self._get_save_path else os.getcwd()
        base = type(self).__name__.replace("App", "").lower()
        return os.path.join(save_dir, f"{base}.txt")

    def start_count(self):
        if self._count_proc and self._count_proc.poll() is None:
            return

        # 카운트 시작 시 파일 초기화 (덮어쓰기)
        try:
            with open(self._file_path(), "w", encoding="utf-8") as f:
                f.write("")
        except Exception as e:
            print(f"[count file init error] {e}")

        worker = os.path.join(os.path.dirname(__file__), 'count_worker.py')
        self._count_proc = subprocess.Popen(
            [sys.executable, worker],
            stdout=subprocess.PIPE,
            text=True
        )
        self.count_label.setText("0")
        self._count_timer.start()

    def _poll_count(self):
        if self._count_proc is None:
            self._count_timer.stop()
            return

        line = self._count_proc.stdout.readline()
        if line and line.strip():
            value = line.strip()
            self.count_label.setText(value)
            # 숫자 들어오는 즉시 파일에 append
            try:
                with open(self._file_path(), "a", encoding="utf-8") as f:
                    f.write(value + "\n")
            except Exception as e:
                print(f"[count write error] {e}")

        if self._count_proc.poll() is not None:
            # 프로세스 종료 후 남은 출력 처리
            for line in self._count_proc.stdout:
                if line.strip():
                    value = line.strip()
                    self.count_label.setText(value)
                    try:
                        with open(self._file_path(), "a", encoding="utf-8") as f:
                            f.write(value + "\n")
                    except Exception as e:
                        print(f"[count write error] {e}")
            self._count_timer.stop()
            self._count_proc = None
