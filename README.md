# AppDrawer 프로젝트

PyQt5 기반의 앱 런처 GUI 애플리케이션

## 프로젝트 개요

확장/축소 가능한 사이드바를 가진 앱 런처로, 여러 개의 독립적인 앱들을 메인 창 또는 팝업 창에서 실행할 수 있습니다.

## 주요 기능

### 1. 사이드바
- 토글 버튼(☰)으로 넓게(200px) / 좁게(60px) 전환 가능
- 3개의 메뉴: Apps(📱), Settings(⚙️), Profile(👤)
- 선택된 메뉴는 하이라이트 표시

### 2. Apps 메뉴
- 선택 시 그리드 형태를 가진 탭 위젯 형태로 표시.
- 탭은 기본 탭과 다음 탭은 '+' 형태로 누르면 새로운 탭이 추가되면서 그 안에 동일하게 그리드 앱들이 표시 되도록.
- 처음 탭과 추가된 탭은 동일한 그리드 앱들을 보여주며 탭을 추가하면 계속 그리드 앱들이 보이고 선택하면 수행 되도록.
- 앱들은 그리드 형태로 앱 카드 표시 (150x150px)
- 앱을 수행하면 탭 창 안에서 개별적으로 수행 되도록, 즉 탭 마다 앱들을 동시에 표시할 수 있음.
- 좌클릭: 메인 창에서 앱 실행 (뒤로가기 버튼으로 앱 목록 복귀)
- 우클릭: 별도 팝업 창으로 앱 실행

### 3. 앱 구조
각 앱은 독립적인 폴더 구조를 가지며, .ui 파일과 .py 파일로 구성됩니다.

## 프로젝트 구조

```
AppDrawer/
├── main.py                 # 메인 애플리케이션
├── mainwindow.ui           # 메인 윈도우 UI
├── requirements.txt        # 의존성 패키지
├── README.md              # 프로젝트 문서
└── Apps/                  # 앱 폴더
    ├── Calculator/        # 계산기 앱
    │   ├── calculator.py
    │   └── calculator.ui
    ├── Notes/            # 메모장 앱
    │   ├── notes.py
    │   └── notes.ui
    ├── Weather/          # 날씨 앱
    │   ├── weather.py
    │   └── weather.ui
    └── Todo/             # 할일 목록 앱
        ├── todo.py
        └── todo.ui
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

## 구현된 앱

### 1. 계산기 (Calculator)
- 기본 사칙연산 (+, -, ×, ÷)
- 소수점 계산 지원
- 퍼센트 계산 (%)
- 백스페이스 기능 (⌫)
- 초기화 기능 (C)
- 0으로 나누기 에러 처리
- 완전히 작동하는 계산기

### 2. 메모장 (Notes)
- UI만 구현됨
- 텍스트 편집 영역
- 저장/지우기 버튼

### 3. 날씨 (Weather)
- UI만 구현됨
- 날씨 아이콘 표시 영역
- 온도 표시 영역

### 4. 할일 목록 (Todo)
- UI만 구현됨
- 할일 입력 필드
- 할일 목록 표시 영역

## 새로운 앱 추가 방법

### 1. 앱 폴더 생성
```
Apps/
└── NewApp/
    ├── newapp.py
    └── newapp.ui
```

### 2. UI 파일 작성 (newapp.ui)
Qt Designer를 사용하거나 XML로 직접 작성

### 3. Python 파일 작성 (newapp.py)
```python
import os
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

class NewApp(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'newapp.ui')
        loadUi(ui_path, self)
        
        # 시그널 연결 및 초기화
        self.setup_ui()
    
    def setup_ui(self):
        # 버튼 연결 등
        pass
```

### 4. main.py에 앱 등록
```python
# 임포트 추가
from Apps.NewApp.newapp import NewApp

# MainWindow 클래스의 __init__에서 앱 레지스트리에 추가
self.apps = {
    "계산기": CalculatorApp,
    "메모장": NotesApp,
    "날씨": WeatherApp,
    "할일 목록": TodoApp,
    "새 앱": NewApp  # 추가
}
```

## 기술 스택

- Python 3.x
- PyQt5: GUI 프레임워크
- Qt Designer: UI 디자인 (.ui 파일)

## UI 디자인 가이드

### 색상 스키마
- 사이드바 배경: #2c3e50
- 사이드바 호버: rgba(255, 255, 255, 0.1)
- 사이드바 선택: rgba(255, 255, 255, 0.2)
- 앱 카드 배경: #f0f0f0
- 앱 카드 테두리: #ddd
- 앱 카드 호버 테두리: #4CAF50

### 레이아웃
- 사이드바 넓이: 200px (확장) / 60px (축소)
- 앱 카드 크기: 150x150px
- 앱 그리드 간격: 20px

## 향후 개발 계획

- [ ] 메모장 앱 기능 구현
- [ ] 날씨 앱 API 연동
- [ ] 할일 목록 앱 기능 구현
- [ ] 앱 설정 저장/불러오기
- [ ] 사용자 프로필 관리
- [ ] 앱 아이콘 커스터마이징
- [ ] 앱 검색 기능
- [ ] 최근 사용 앱 표시
'appDrawer' 
