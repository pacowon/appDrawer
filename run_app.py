# -*- coding: utf-8 -*-
"""
독립 프로세스로 단일 앱을 실행하는 런처.
사용법: python run_app.py <앱이름> [작업경로]
"""
import sys
import os
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_app.py <app_name> [work_dir]")
        sys.exit(1)

    app_name = sys.argv[1]
    work_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()

    # 작업 경로 적용
    try:
        os.chdir(work_dir)
    except Exception:
        pass

    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
    from appSetting import APP_REGISTRY, get_app_config

    if app_name not in APP_REGISTRY:
        print(f"Unknown app: {app_name}")
        sys.exit(1)

    app_config = get_app_config(APP_REGISTRY[app_name])
    if app_config["type"] == "script":
        script_path = app_config.get("script")
        if not script_path:
            print(f"Script path is missing for app: {app_name}")
            sys.exit(1)

        script_abspath = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), script_path)
        )
        subprocess.Popen([sys.executable, script_abspath], cwd=work_dir)
        sys.exit(0)
    if app_config["type"] == "command":
        command = app_config.get("command")
        if not command:
            print(f"Command is missing for app: {app_name}")
            sys.exit(1)

        if os.name == "nt":
            subprocess.Popen(command, cwd=work_dir, shell=True)
        else:
            subprocess.Popen(["/bin/bash", "-lc", command], cwd=work_dir)
        sys.exit(0)

    app = QApplication(sys.argv)

    app_class = app_config["app_class"]
    window = QWidget()
    window.setWindowTitle(app_name)
    window.resize(600, 480)
    layout = QVBoxLayout(window)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(app_class())
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
