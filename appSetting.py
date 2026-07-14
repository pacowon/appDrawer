# -*- coding: utf-8 -*-
"""
앱 등록 설정 파일.
실제 존재하는 앱만 APP_REGISTRY에 등록한다.
형식: "앱 이름": (AppClass, "이니셜2글자")
"""
from Apps.AgeCalc.age_calc import AgeCalcApp
from Apps.Base64Tool.base64_tool import Base64ToolApp
from Apps.BMICalc.bmi_calc import BMICalcApp
from Apps.ButtonGallery.button_gallery import ButtonGalleryApp
from Apps.Calculator.calculator import CalculatorApp
from Apps.Clock.clock import ClockApp
from Apps.ColorMixer.color_mixer import ColorMixerApp
from Apps.ColorPicker.color_picker import ColorPickerApp
from Apps.Compass.compass import CompassApp
from Apps.Counter.counter import CounterApp
from Apps.CurrencyCalc.currency_calc import CurrencyCalcApp
from Apps.DiceRoller.dice_roller import DiceRollerApp
from Apps.Flipcoin.flipcoin import FlipcoinApp
from Apps.HashGen.hash_gen import HashGenApp
from Apps.Morse.morse import MorseApp
from Apps.Notes.notes import NotesApp
from Apps.NumberGuess.number_guess import NumberGuessApp
from Apps.PasswordGen.password_gen import PasswordGenApp
from Apps.Pomodoro.pomodoro import PomodoroApp
from Apps.QuoteOfDay.quote_of_day import QuoteOfDayApp
from Apps.RandomPick.random_pick import RandomPickApp
from Apps.RockPaperScissors.rps import RockPaperScissorsApp


def script_app(script_path, icon):
    return {
        "type": "script",
        "script": script_path,
        "icon": icon,
    }


def command_app(command, icon):
    return {
        "type": "command",
        "command": command,
        "icon": icon,
    }


def terminal_app(command, icon):
    return {
        "type": "terminal",
        "command": command,
        "icon": icon,
    }


def get_app_config(app_entry):
    if isinstance(app_entry, tuple):
        app_class, icon = app_entry
        return {
            "type": "widget",
            "app_class": app_class,
            "script": None,
            "command": None,
            "icon": icon,
        }
    if isinstance(app_entry, dict):
        return {
            "type": str(app_entry.get("type", "widget")),
            "app_class": app_entry.get("app_class"),
            "script": app_entry.get("script"),
            "command": app_entry.get("command"),
            "icon": app_entry.get("icon", "AP"),
        }
    raise TypeError(f"Unsupported app entry: {app_entry!r}")

# Example:
# "Some Script App": script_app("Apps/SomeScript/run.py", "SS"),
# "Some Shell Script": script_app("sh /path/code.sh", "SH"),
# "Some Command App": command_app("/path/to/launcher -- /path/to/app.py &", "CM"),
# "Some TUI App": terminal_app("htop", "HT"),
APP_REGISTRY = {
    "계산기": (CalculatorApp, "CA"),
    "메모장": (NotesApp, "NT"),
    "시계": (ClockApp, "CL"),
    "주사위": (DiceRollerApp, "DR"),
    "색상 선택": (ColorPickerApp, "CP"),
    "버튼 갤러리": (ButtonGalleryApp, "BG"),
    "동전 던지기": (FlipcoinApp, "FC"),
    "랜덤 선택": (RandomPickApp, "RP"),
    "카운터": (CounterApp, "CT"),
    "BMI 계산": (BMICalcApp, "BM"),
    "나이 계산": (AgeCalcApp, "AG"),
    "비밀번호": (PasswordGenApp, "PW"),
    "나침반": (CompassApp, "CM"),
    "모스 부호": (MorseApp, "MO"),
    "포모도로": (PomodoroApp, "PM"),
    "해시 생성": (HashGenApp, "HS"),
    "Base64": (Base64ToolApp, "B6"),
    "숫자 맞추기": (NumberGuessApp, "NG"),
    "가위바위보": (RockPaperScissorsApp, "RK"),
    "환율 계산": (CurrencyCalcApp, "FX"),
    "오늘의 명언": (QuoteOfDayApp, "QT"),
    "색상 믹서": (ColorMixerApp, "MX"),
    "Script Note": script_app("Apps/ScriptNote/run.py", "SN"),
    "Script Path": script_app("Apps/ScriptPathViewer/run.py", "SP"),
    "Terminal Sample": terminal_app("pwd; ls -la; echo; read -p 'Press Enter to close...'", "TS"),
}
