"""
앱 등록 설정 파일.
새 앱 추가 시 이 파일만 수정하면 됩니다.
형식: "앱 이름": (AppClass, "이니셜2글자")
"""
from Apps.Calculator.calculator import CalculatorApp
from Apps.Notes.notes import NotesApp
from Apps.Weather.weather import WeatherApp
from Apps.Todo.todo import TodoApp
from Apps.Clock.clock import ClockApp
from Apps.Stopwatch.stopwatch import StopwatchApp
from Apps.DiceRoller.dice_roller import DiceRollerApp
from Apps.TextCounter.text_counter import TextCounterApp
from Apps.UnitConverter.unit_converter import UnitConverterApp
from Apps.ColorPicker.color_picker import ColorPickerApp
from Apps.ButtonGallery.button_gallery import ButtonGalleryApp
from Apps.Flipcoin.flipcoin import FlipcoinApp
from Apps.RandomPick.random_pick import RandomPickApp
from Apps.Counter.counter import CounterApp
from Apps.BMICalc.bmi_calc import BMICalcApp
from Apps.AgeCalc.age_calc import AgeCalcApp
from Apps.PasswordGen.password_gen import PasswordGenApp
from Apps.TipCalc.tip_calc import TipCalcApp
from Apps.Compass.compass import CompassApp
from Apps.Morse.morse import MorseApp
from Apps.Pomodoro.pomodoro import PomodoroApp
from Apps.HashGen.hash_gen import HashGenApp
from Apps.Base64Tool.base64_tool import Base64ToolApp
from Apps.NumberGuess.number_guess import NumberGuessApp
from Apps.RockPaperScissors.rps import RockPaperScissorsApp
from Apps.SpeedTyping.speed_typing import SpeedTypingApp
from Apps.CurrencyCalc.currency_calc import CurrencyCalcApp
from Apps.QuoteOfDay.quote_of_day import QuoteOfDayApp
from Apps.ColorMixer.color_mixer import ColorMixerApp
from Apps.WorldClock.world_clock import WorldClockApp

APP_REGISTRY = {
    "계산기":       (CalculatorApp,         "CA"),
    "메모장":       (NotesApp,              "NT"),
    "날씨":         (WeatherApp,            "WE"),
    "할일 목록":    (TodoApp,               "TD"),
    "시계":         (ClockApp,              "CL"),
    "스톱워치":     (StopwatchApp,          "SW"),
    "주사위":       (DiceRollerApp,         "DR"),
    "글자 수":      (TextCounterApp,        "TC"),
    "단위 변환":    (UnitConverterApp,      "UC"),
    "색상 선택":    (ColorPickerApp,        "CP"),
    "버튼 갤러리":  (ButtonGalleryApp,      "BG"),
    "동전 던지기":  (FlipcoinApp,           "FC"),
    "랜덤 선택":    (RandomPickApp,         "RP"),
    "카운터":       (CounterApp,            "CT"),
    "BMI 계산":     (BMICalcApp,            "BM"),
    "나이 계산":    (AgeCalcApp,            "AG"),
    "비밀번호":     (PasswordGenApp,        "PW"),
    "팁 계산":      (TipCalcApp,            "TP"),
    "나침반":       (CompassApp,            "CM"),
    "모스 부호":    (MorseApp,              "MO"),
    "포모도로":     (PomodoroApp,           "PM"),
    "해시 생성":    (HashGenApp,            "HS"),
    "Base64":       (Base64ToolApp,         "B6"),
    "숫자 맞추기":  (NumberGuessApp,        "NG"),
    "가위바위보":   (RockPaperScissorsApp,  "RK"),
    "타이핑 테스트":(SpeedTypingApp,        "ST"),
    "환율 계산":    (CurrencyCalcApp,       "FX"),
    "오늘의 명언":  (QuoteOfDayApp,         "QT"),
    "색상 믹서":    (ColorMixerApp,         "MX"),
    "세계 시계":    (WorldClockApp,         "WC"),
}
