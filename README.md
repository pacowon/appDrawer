# AppDrawer 프로젝트

PyQt5 기반의 탭형 앱 런처 GUI 애플리케이션입니다.

## 프로젝트 개요

AppDrawer는 여러 개의 독립적인 미니 앱을 하나의 메인 창에서 관리하고 실행할 수 있는 데스크톱 런처입니다.

- 확장/축소 가능한 사이드바 제공
- 탭 단위로 앱 목록과 앱 실행 화면 분리
- 앱 카드를 드래그해서 순서 변경 가능
- 좌클릭은 현재 탭에서 실행, 우클릭은 별도 팝업 프로세스로 실행
- 탭마다 작업 경로를 따로 선택 가능

## 현재 구현 상태

### 사이드바
- `Apps`, `Settings`, `Profile` 3개 메뉴
- 토글 버튼으로 `200px / 60px` 너비 전환
- 선택된 메뉴 하이라이트

### Apps 화면
- `QTabWidget` 기반 다중 탭 구조
- 마지막 `+` 탭 선택 시 새 앱 목록 탭 자동 생성
- 각 탭은 동일한 앱 그리드를 가짐
- 앱 카드는 드래그 앤 드롭으로 재정렬 가능
- 정렬 순서는 사용자 홈 경로의 `.appdrawer_order.json`에 저장

### 앱 실행
- 좌클릭: 현재 탭 내부에서 앱 실행
- 뒤로가기 버튼으로 앱 목록 복귀
- 우클릭: `run_app.py`로 별도 프로세스 실행
- 각 탭 하단 `PathBar`에서 작업 경로 선택 가능

### 공통 기능
- 대부분의 앱이 `CountMixin`을 사용
- `Count` 버튼을 누르면 서브프로세스가 1부터 20까지 카운트
- 카운트 결과는 현재 탭의 작업 경로에 `<appname>.txt`로 저장
- `📂 경로` 버튼으로 현재 저장 경로 확인 가능

## 프로젝트 구조

```text
AppDrawer/
├── main.py
├── appSetting.py
├── run_app.py
├── icon.py
├── mainwindow.ui
├── requirements.txt
├── README.md
└── Apps/
    ├── path_bar.py
    ├── count_mixin.py
    ├── count_worker.py
    ├── Calculator/
    ├── Notes/
    ├── Clock/
    ├── DiceRoller/
    ├── ColorPicker/
    ├── ButtonGallery/
    ├── Flipcoin/
    ├── RandomPick/
    ├── Counter/
    ├── BMICalc/
    ├── AgeCalc/
    ├── PasswordGen/
    ├── Compass/
    ├── Morse/
    ├── Pomodoro/
    ├── HashGen/
    ├── Base64Tool/
    ├── NumberGuess/
    ├── RockPaperScissors/
    ├── CurrencyCalc/
    ├── QuoteOfDay/
    └── ColorMixer/
```

## 등록된 앱

현재 `appSetting.py`에 등록된 앱은 아래와 같습니다.

- 계산기
- 메모장
- 시계
- 주사위
- 색상 선택
- 버튼 갤러리
- 동전 던지기
- 랜덤 선택
- 카운터
- BMI 계산
- 나이 계산
- 비밀번호
- 나침반
- 모스 부호
- 포모도로
- 해시 생성
- Base64
- 숫자 맞추기
- 가위바위보
- 환율 계산
- 오늘의 명언
- 색상 믹서

## 앱 추가 방법

### 1. 앱 폴더 생성

```text
Apps/
└── NewApp/
    ├── new_app.py
    └── new_app.ui
```

### 2. 앱 클래스 작성

```python
import os
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

class NewApp(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(os.path.dirname(__file__), "new_app.ui"), self)
```

`CountMixin`을 쓰려면 `btn_count`, `count_label`, 선택적으로 `btn_show_path`를 UI에 두고 `self.setup_count()`를 호출하면 됩니다.

### 3. 레지스트리 등록

새 앱은 `main.py`가 아니라 `appSetting.py`의 `APP_REGISTRY`에 등록합니다.

```python
from Apps.NewApp.new_app import NewApp

APP_REGISTRY = {
    "새 앱": (NewApp, "NA"),
}
```

## 설치 및 실행

### 요구사항
- Python 3.7 이상
- PyQt5 5.15.0 이상

### 설치

```bash
cd AppDrawer
pip install -r requirements.txt
```

### 실행

```bash
python main.py
```

## 기술 스택

- Python 3.x
- PyQt5
- Qt Designer

## 향후 개선 아이디어

- Settings/Profile 실제 기능 추가
- 앱 검색 기능
- 최근 사용 앱 표시
- 아이콘 커스터마이징
- 앱 메타데이터 자동 스캔 등록
- 탭별 상태 저장
