"""
독립 프로세스로 단일 앱을 실행하는 런처.
사용법: python run_app.py <앱이름> [작업경로]
"""
import sys
import os

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
    from appSetting import APP_REGISTRY

    if app_name not in APP_REGISTRY:
        print(f"Unknown app: {app_name}")
        sys.exit(1)

    app = QApplication(sys.argv)

    app_class, _ = APP_REGISTRY[app_name]
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
