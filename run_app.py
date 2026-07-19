# -*- coding: utf-8 -*-
"""
독립 프로세스로 단일 앱을 실행하는 런처.
사용법: python run_app.py <앱이름> [작업경로]
"""
import sys
import os
import subprocess
import shutil
import shlex

os.environ.setdefault("NO_AT_BRIDGE", "1")
if os.name != "nt":
    os.environ.setdefault("QT_IM_MODULE", "ibus")
    os.environ.setdefault("GTK_IM_MODULE", "ibus")
    os.environ.setdefault("XMODIFIERS", "@im=ibus")


def launch_env():
    env = os.environ.copy()
    env.setdefault("NO_AT_BRIDGE", "1")
    if os.name != "nt":
        env.setdefault("QT_IM_MODULE", "ibus")
        env.setdefault("GTK_IM_MODULE", "ibus")
        env.setdefault("XMODIFIERS", "@im=ibus")
    lang = env.get("LANG", "")
    if "UTF-8" not in lang.upper() and "UTF8" not in lang.upper():
        env["LANG"] = "C.UTF-8"
    for key in ("LC_CTYPE", "LC_ALL"):
        value = env.get(key, "")
        if value and "UTF-8" not in value.upper() and "UTF8" not in value.upper():
            env.pop(key, None)
    env.setdefault("LC_CTYPE", env["LANG"])
    return env


def xterm_font_family():
    candidates = [
        "D2Coding",
        "NanumGothicCoding",
        "Nanum Gothic Coding",
        "NanumBarunGothic",
        "Noto Sans Mono CJK KR",
        "Noto Sans CJK KR",
        "Baekmuk Gulim",
        "Malgun Gothic",
        "UnDotum",
        "DejaVu Sans Mono",
    ]
    if os.name != "nt" and shutil.which("fc-match"):
        for family in candidates:
            try:
                matched = subprocess.check_output(
                    ["fc-match", "-f", "%{family}", family],
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=0.5,
                )
            except Exception:
                continue
            matched_names = [name.strip() for name in matched.split(",")]
            if family in matched_names:
                return family
        try:
            matched = subprocess.check_output(
                ["fc-match", "-f", "%{family}", "monospace:lang=ko"],
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=0.5,
            )
            family = matched.split(",")[0].strip()
            if family:
                return family
        except Exception:
            pass
    return "Noto Sans Mono CJK KR"


def xterm_utf8_args():
    return [
        "-u8",
        "-lc",
        "-xim",
        "-xrm", "XTerm*utf8: 1",
        "-xrm", "XTerm*locale: true",
        "-xrm", "XTerm*openIm: true",
        "-xrm", "XTerm*inputMethod: ibus",
        "-xrm", "XTerm*preeditType: OverTheSpot",
    ]


def run_shell_command(command, work_dir):
    if os.name == "nt":
        subprocess.Popen(command, cwd=work_dir, shell=True, env=launch_env())
    else:
        subprocess.Popen(["/bin/bash", "-lc", command], cwd=work_dir, env=launch_env())


def run_script_entry(script_path, script_abspath, work_dir):
    if os.path.isfile(script_abspath):
        if script_abspath.lower().endswith(".py"):
            subprocess.Popen([sys.executable, script_abspath], cwd=work_dir, env=launch_env())
        elif os.name != "nt" and os.access(script_abspath, os.X_OK):
            subprocess.Popen([script_abspath], cwd=work_dir, env=launch_env())
        elif os.name == "nt":
            subprocess.Popen([script_abspath], cwd=work_dir, shell=True, env=launch_env())
        else:
            run_shell_command(shlex.quote(script_abspath), work_dir)
        return

    run_shell_command(script_path, work_dir)


def interactive_shell_path():
    shell = os.environ.get("SHELL")
    if shell and os.path.exists(shell):
        return shell
    return "/bin/bash"


def terminal_shell_command(command, shell):
    shell_name = os.path.basename(shell)
    quoted_shell = shlex.quote(shell)

    if shell_name in {"fish"}:
        return (
            f"{command}\n"
            "set appdrawer_status $status\n"
            "echo\n"
            "echo \"[AppDrawer] Command exited with status $appdrawer_status.\"\n"
            "echo \"[AppDrawer] Starting an interactive shell. Type 'exit' to close this terminal.\"\n"
            f"exec {quoted_shell} -i"
        )

    if shell_name in {"csh", "tcsh"}:
        return (
            f"{command}\n"
            "set appdrawer_status = $status\n"
            "echo\n"
            "echo \"[AppDrawer] Command exited with status $appdrawer_status.\"\n"
            "echo \"[AppDrawer] Starting an interactive shell. Type 'exit' to close this terminal.\"\n"
            f"exec {quoted_shell} -i"
        )

    return (
        f"{command}\n"
        "status=$?\n"
        "echo\n"
        "echo \"[AppDrawer] Command exited with status ${status}.\"\n"
        "echo \"[AppDrawer] Starting an interactive shell. Type 'exit' to close this terminal.\"\n"
        f"exec {quoted_shell} -i"
    )


def run_terminal_command(command, work_dir):
    if os.name == "nt":
        subprocess.Popen(f'start cmd /k "{command}"', cwd=work_dir, shell=True, env=launch_env())
        return

    shell = interactive_shell_path()
    terminal_command = terminal_shell_command(command, shell)
    terminal = os.environ.get("TERMINAL")
    if terminal and shutil.which(terminal):
        if os.path.basename(terminal) == "xterm":
            args = [terminal] + xterm_utf8_args() + ["-e", shell, "-ic", terminal_command]
        else:
            args = [terminal, "-e", shell, "-ic", terminal_command]
        subprocess.Popen(args, cwd=work_dir, env=launch_env())
        return

    launchers = [
        ("x-terminal-emulator", ["x-terminal-emulator", "-e", shell, "-ic", terminal_command]),
        ("gnome-terminal", ["gnome-terminal", "--", shell, "-ic", terminal_command]),
        ("konsole", ["konsole", "-e", shell, "-ic", terminal_command]),
        ("xfce4-terminal", ["xfce4-terminal", "--command", f"{shlex.quote(shell)} -ic {shlex.quote(terminal_command)}"]),
        ("lxterminal", ["lxterminal", "-e", shell, "-ic", terminal_command]),
        ("mate-terminal", ["mate-terminal", "--", shell, "-ic", terminal_command]),
        ("xterm", ["xterm"] + xterm_utf8_args() + ["-e", shell, "-ic", terminal_command]),
    ]
    for executable, args in launchers:
        if shutil.which(executable):
            subprocess.Popen(args, cwd=work_dir, env=launch_env())
            return

    print("No supported terminal emulator found; running command without a new terminal.")
    run_shell_command(command, work_dir)


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

        app_root = os.path.dirname(os.path.abspath(__file__))
        script_abspath = (
            script_path
            if os.path.isabs(script_path)
            else os.path.abspath(os.path.join(app_root, script_path))
        )
        run_script_entry(script_path, script_abspath, work_dir)
        sys.exit(0)
    if app_config["type"] == "command":
        command = app_config.get("command")
        if not command:
            print(f"Command is missing for app: {app_name}")
            sys.exit(1)

        run_shell_command(command, work_dir)
        sys.exit(0)
    if app_config["type"] == "terminal":
        command = app_config.get("command")
        if not command:
            print(f"Terminal command is missing for app: {app_name}")
            sys.exit(1)

        run_terminal_command(command, work_dir)
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
