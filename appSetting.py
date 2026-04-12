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
}

THEMES = {
    "light": {
        "label": "Light",
        "window_bg": "#f5f7fb",
        "page_bg": "#ffffff",
        "panel_bg": "#ffffff",
        "panel_alt_bg": "#eef2f7",
        "border": "#d8dee8",
        "text": "#223046",
        "muted_text": "#6b7a90",
        "sidebar_bg": "#2c3e50",
        "sidebar_hover": "rgba(255,255,255,0.10)",
        "sidebar_checked": "rgba(255,255,255,0.20)",
        "sidebar_text": "#ffffff",
        "accent": "#3498db",
        "accent_hover": "#2980b9",
        "input_bg": "#ffffff",
        "card_bg": "#f0f4f8",
        "card_hover_bg": "#e7edf5",
        "card_border": "#d5dde7",
        "card_hover_border": "#3498db",
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
    "dark": {
        "label": "Dark",
        "window_bg": "#11161d",
        "page_bg": "#17202b",
        "panel_bg": "#1d2733",
        "panel_alt_bg": "#243140",
        "border": "#314050",
        "text": "#ecf2f8",
        "muted_text": "#9db0c3",
        "sidebar_bg": "#0e141b",
        "sidebar_hover": "rgba(255,255,255,0.08)",
        "sidebar_checked": "rgba(255,255,255,0.16)",
        "sidebar_text": "#f5f8fc",
        "accent": "#4db6ff",
        "accent_hover": "#3595d6",
        "input_bg": "#243140",
        "card_bg": "#223040",
        "card_hover_bg": "#2a3a4c",
        "card_border": "#3a4b5d",
        "card_hover_border": "#4db6ff",
        "path_bg": "#233040",
        "path_border": "#36485a",
        "path_text": "#ecf2f8",
        "path_button_bg": "#4db6ff",
        "path_button_hover": "#3595d6",
        "path_button_text": "#08131f",
        "path_button_disabled_bg": "#55697d",
        "path_button_disabled_text": "#d0dae4",
        "path_disabled_bg": "#1b2632",
        "path_disabled_border": "#36485a",
    },
    "pink": {
        "label": "Pink",
        "window_bg": "#ffc7e1",
        "page_bg": "#ffd8ea",
        "panel_bg": "#ffe4f0",
        "panel_alt_bg": "#ffc6df",
        "border": "#f5bdd7",
        "text": "#5e2341",
        "muted_text": "#b0678d",
        "sidebar_bg": "#ff6fb0",
        "sidebar_hover": "rgba(255,255,255,0.20)",
        "sidebar_checked": "rgba(255,255,255,0.30)",
        "sidebar_text": "#fff8fc",
        "accent": "#ff4fa0",
        "accent_hover": "#f0338f",
        "input_bg": "#ffedf6",
        "card_bg": "#ffe0ee",
        "card_hover_bg": "#ffcfe3",
        "card_border": "#f8bfd9",
        "card_hover_border": "#ff4fa0",
        "path_bg": "#ffd9eb",
        "path_border": "#f2b3d1",
        "path_text": "#6d2850",
        "path_button_bg": "#ff4fa0",
        "path_button_hover": "#f0338f",
        "path_button_text": "#ffffff",
        "path_button_disabled_bg": "#e3a8c5",
        "path_button_disabled_text": "#fff6fb",
        "path_disabled_bg": "#f8cade",
        "path_disabled_border": "#ebb0cd",
    },
    "sunset": {
        "label": "Sunset",
        "window_bg": "#fff2e8",
        "page_bg": "#fffaf6",
        "panel_bg": "#ffffff",
        "panel_alt_bg": "#ffe8d7",
        "border": "#f1c9ae",
        "text": "#4b2d1f",
        "muted_text": "#8f6853",
        "sidebar_bg": "#4a2f2a",
        "sidebar_hover": "rgba(255,255,255,0.10)",
        "sidebar_checked": "rgba(255,255,255,0.18)",
        "sidebar_text": "#fff7f2",
        "accent": "#e67e22",
        "accent_hover": "#cf6d15",
        "input_bg": "#ffffff",
        "card_bg": "#fff2e5",
        "card_hover_bg": "#ffe7d3",
        "card_border": "#f0cfb4",
        "card_hover_border": "#e67e22",
        "path_bg": "#f8e3d4",
        "path_border": "#e3bfa4",
        "path_text": "#4b2d1f",
        "path_button_bg": "#e67e22",
        "path_button_hover": "#cf6d15",
        "path_button_text": "#ffffff",
        "path_button_disabled_bg": "#cfb39f",
        "path_button_disabled_text": "#fff7f2",
        "path_disabled_bg": "#efd5c5",
        "path_disabled_border": "#d8b198",
    },
}
