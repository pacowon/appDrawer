import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, 
                             QScrollArea, QGridLayout, QDialog, QStackedWidget,
                             QTabWidget, QTabBar)
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData, QPoint, QSize
from PyQt5.QtGui import QFont, QDrag, QPixmap, QPainter, QColor
from PyQt5.uic import loadUi

# 앱 임포트
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
from Apps.path_bar import AppContainer
from icon import make_heart_icon

# 앱 카드 위젯
class AppCard(QFrame):
    clicked = pyqtSignal(str)
    rightClicked = pyqtSignal(str)
    
    def __init__(self, app_name, app_class, icon="📱"):
        super().__init__()
        self.app_name = app_name
        self.app_class = app_class
        self.icon = icon
        self._drag_start_pos = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setFixedSize(130, 130)
        self.setCursor(Qt.PointingHandCursor)

        # 앱마다 고유 배경색 (이니셜 해시 기반)
        hue = (hash(self.app_name) % 12) * 30          # 0~330, 30 단위
        colors = [
            "#e74c3c","#e67e22","#f1c40f","#2ecc71",
            "#1abc9c","#3498db","#2980b9","#9b59b6",
            "#8e44ad","#e91e63","#00bcd4","#ff5722",
        ]
        bg_color = colors[hash(self.app_name) % len(colors)]

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(4)

        # 이니셜 배지 (원형 배경 + 흰 텍스트)
        badge = QLabel(self.icon)          # icon 필드에 이니셜 2글자 저장
        badge.setAlignment(Qt.AlignCenter)
        badge.setFixedSize(64, 64)
        badge.setFont(QFont("Arial", 20, QFont.Bold))
        badge.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: white;
                border-radius: 32px;
            }}
        """)

        name_label = QLabel(self.app_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFont(QFont("Arial", 10))
        name_label.setWordWrap(True)

        layout.addWidget(badge, 0, Qt.AlignHCenter)
        layout.addWidget(name_label)
        self.setLayout(layout)
        self._apply_style(False)
    
    def _apply_style(self, dragging):
        if dragging:
            self.setStyleSheet("""
                AppCard {
                    background-color: #c8e6c9;
                    border-radius: 10px;
                    border: 2px dashed #4CAF50;
                }
            """)
        else:
            self.setStyleSheet("""
                AppCard {
                    background-color: #f0f0f0;
                    border-radius: 10px;
                    border: 2px solid #ddd;
                }
                AppCard:hover {
                    background-color: #e0e0e0;
                    border: 2px solid #4CAF50;
                }
            """)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = event.pos()
        elif event.button() == Qt.RightButton:
            self.rightClicked.emit(self.app_name)
    
    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if self._drag_start_pos is None:
            return
        if (event.pos() - self._drag_start_pos).manhattanLength() < QApplication.startDragDistance():
            return
        
        # 드래그 시작
        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(self.app_name)
        drag.setMimeData(mime)
        
        # 드래그 중 카드 미리보기 이미지
        pixmap = QPixmap(self.size())
        pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pixmap)
        painter.setOpacity(0.7)
        self.render(painter)
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        
        self._apply_style(True)
        drag.exec_(Qt.MoveAction)
        self._apply_style(False)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 드래그 없이 클릭만 한 경우
            if self._drag_start_pos is not None:
                if (event.pos() - self._drag_start_pos).manhattanLength() < QApplication.startDragDistance():
                    self.clicked.emit(self.app_name)
            self._drag_start_pos = None

# 드래그 앤 드롭 가능한 앱 그리드
class AppGrid(QWidget):
    def __init__(self, apps, on_click, on_right_click):
        super().__init__()
        self.apps = apps
        self.app_order = list(apps.keys())
        self.on_click = on_click
        self.on_right_click = on_right_click
        self.setAcceptDrops(True)
        
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        
        self._drop_indicator = None
        self.rebuild_grid()
    
    def rebuild_grid(self):
        # 기존 위젯 제거
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        cols = 5
        for i, app_name in enumerate(self.app_order):
            app_class, icon = self.apps[app_name]
            card = AppCard(app_name, app_class, icon)
            card.clicked.connect(self.on_click)
            card.rightClicked.connect(self.on_right_click)
            self.grid_layout.addWidget(card, i // cols, i % cols)
        
        rows = (len(self.app_order) + cols - 1) // cols
        self.grid_layout.setRowStretch(rows, 1)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        if not event.mimeData().hasText():
            return
        
        dragged_name = event.mimeData().text()
        drop_pos = event.pos()
        
        # 드롭 위치에서 가장 가까운 카드 인덱스 찾기
        target_index = self._get_drop_index(drop_pos)
        source_index = self.app_order.index(dragged_name)
        
        if target_index != source_index and target_index != -1:
            self.app_order.insert(target_index, self.app_order.pop(source_index))
            self.rebuild_grid()
        
        event.acceptProposedAction()
    
    def _get_drop_index(self, pos):
        cols = 4
        best_index = len(self.app_order) - 1
        best_dist = float('inf')
        
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                center = widget.geometry().center()
                dist = (center - pos).manhattanLength()
                if dist < best_dist:
                    best_dist = dist
                    best_index = i
        
        return best_index


# 사이드바 버튼
class SidebarButton(QPushButton):
    def __init__(self, text, icon_text=""):
        super().__init__()
        self.full_text = text
        self.icon_text = icon_text
        self.is_expanded = True
        self.setText(f"{icon_text}  {text}")
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 15px;
                border: none;
                background-color: transparent;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:checked {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
    
    def update_text(self, expanded):
        self.is_expanded = expanded
        if expanded:
            self.setText(f"{self.icon_text}  {self.full_text}")
        else:
            self.setText(self.icon_text)

# 메인 윈도우
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'mainwindow.ui')
        loadUi(ui_path, self)
        
        # 앱 레지스트리 (이름: (클래스, 이니셜))
        self.apps = {
            "계산기":    (CalculatorApp,    "CA"),
            "메모장":    (NotesApp,         "NT"),
            "날씨":      (WeatherApp,       "WE"),
            "할일 목록": (TodoApp,          "TD"),
            "시계":      (ClockApp,         "CL"),
            "스톱워치":  (StopwatchApp,     "SW"),
            "주사위":    (DiceRollerApp,    "DR"),
            "글자 수":   (TextCounterApp,   "TC"),
            "단위 변환": (UnitConverterApp, "UC"),
            "색상 선택": (ColorPickerApp,   "CP"),
        }
        
        self.setup_ui()
        self._popups = set()  # 팝업 창 참조 유지
        
    def setup_ui(self):
        # 사이드바 설정
        self.sidebar_expanded = True
        
        # 메뉴 버튼들 설정
        self.btn_apps.clicked.connect(self.show_apps)
        self.btn_settings.clicked.connect(self.show_settings)
        self.btn_profile.clicked.connect(self.show_profile)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        
        # Apps 페이지에 탭 위젯 추가
        self.setup_apps_tabs()
        
        # 초기 상태
        self.btn_apps.setChecked(True)
        self.content_stack.setCurrentWidget(self.apps_page)
    
    def setup_apps_tabs(self):
        # 기존 레이아웃 제거
        while self.apps_page_layout.count():
            child = self.apps_page_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # 탭 위젯 생성
        self.apps_tab_widget = QTabWidget()
        self.apps_tab_widget.setTabsClosable(True)
        self.apps_tab_widget.tabCloseRequested.connect(self.close_app_tab)
        self.apps_tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                background: white;
            }
            QTabBar::tab {
                background: #f0f0f0;
                padding: 10px 20px;
                margin-right: 2px;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
            }
            QTabBar::tab:hover {
                background: #e0e0e0;
            }
        """)
        
        # 첫 번째 탭 추가
        self.add_new_app_tab("앱 목록 1")
        
        # '+' 버튼을 위한 더미 탭 추가
        plus_widget = QWidget()
        self.apps_tab_widget.addTab(plus_widget, "+")
        self.apps_tab_widget.tabBar().setTabButton(
            self.apps_tab_widget.count() - 1, 
            QTabBar.RightSide, 
            None
        )
        
        # 탭 변경 시그널 연결
        self.apps_tab_widget.currentChanged.connect(self.on_tab_changed)
        
        self.apps_page_layout.addWidget(self.apps_tab_widget)
    
    def add_new_app_tab(self, tab_name):
        tab_stack = QStackedWidget()
        
        # 앱 그리드 페이지
        grid_page = QWidget()
        grid_page_layout = QVBoxLayout(grid_page)
        grid_page_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        # 드래그 앤 드롭 가능한 그리드
        app_grid = AppGrid(
            self.apps,
            on_click=lambda name, stack=tab_stack, tname=tab_name: self.launch_app_in_tab(name, stack, tname),
            on_right_click=self.launch_app_popup
        )
        
        scroll.setWidget(app_grid)
        grid_page_layout.addWidget(scroll)
        tab_stack.addWidget(grid_page)
        
        insert_index = self.apps_tab_widget.count() - 1
        self.apps_tab_widget.insertTab(insert_index, tab_stack, tab_name)
        self.apps_tab_widget.setCurrentIndex(insert_index)
    
    def launch_app_in_tab(self, app_name, tab_stack, original_tab_name):
        """탭 내에서 앱 실행"""
        tab_index = self.apps_tab_widget.indexOf(tab_stack)
        if tab_index >= 0:
            self.apps_tab_widget.setTabText(tab_index, app_name)

        app_page = QWidget()
        app_layout = QVBoxLayout(app_page)
        app_layout.setContentsMargins(0, 0, 0, 0)

        def go_back():
            tab_stack.setCurrentIndex(0)
            idx = self.apps_tab_widget.indexOf(tab_stack)
            if idx >= 0:
                self.apps_tab_widget.setTabText(idx, original_tab_name)

        back_btn = QPushButton("← 앱 목록으로")
        back_btn.clicked.connect(go_back)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)

        app_widget = self.apps[app_name][0]()
        container = AppContainer(app_widget)

        app_layout.addWidget(back_btn)
        app_layout.addWidget(container, 1)

        while tab_stack.count() > 1:
            widget = tab_stack.widget(1)
            tab_stack.removeWidget(widget)
            widget.deleteLater()

        tab_stack.addWidget(app_page)
        tab_stack.setCurrentIndex(1)
    
    def on_tab_changed(self, index):
        # '+' 탭을 클릭하면 새 탭 추가
        if index == self.apps_tab_widget.count() - 1:
            tab_count = self.apps_tab_widget.count() - 1  # '+' 탭 제외
            self.add_new_app_tab(f"앱 목록 {tab_count + 1}")
    
    def close_app_tab(self, index):
        # 최소 1개의 탭은 유지
        if self.apps_tab_widget.count() > 2:  # 일반 탭 + '+' 탭
            self.apps_tab_widget.removeTab(index)
    
    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar.setFixedWidth(60)
            self.sidebar_expanded = False
        else:
            self.sidebar.setFixedWidth(200)
            self.sidebar_expanded = True
        
        # 버튼 텍스트 업데이트
        if self.sidebar_expanded:
            self.btn_apps.setText("📱  Apps")
            self.btn_settings.setText("⚙️  Settings")
            self.btn_profile.setText("👤  Profile")
        else:
            self.btn_apps.setText("📱")
            self.btn_settings.setText("⚙️")
            self.btn_profile.setText("👤")
    
    def show_apps(self):
        self.content_stack.setCurrentWidget(self.apps_page)
        self.btn_apps.setChecked(True)
        self.btn_settings.setChecked(False)
        self.btn_profile.setChecked(False)
    
    def show_settings(self):
        self.content_stack.setCurrentWidget(self.settings_page)
        self.btn_apps.setChecked(False)
        self.btn_settings.setChecked(True)
        self.btn_profile.setChecked(False)
    
    def show_profile(self):
        self.content_stack.setCurrentWidget(self.profile_page)
        self.btn_apps.setChecked(False)
        self.btn_settings.setChecked(False)
        self.btn_profile.setChecked(True)
    
    def launch_app_inline(self, app_name):
        """메인 창에서 앱 실행 (레거시 - 사용 안 함)"""
        pass
    
    def launch_app_popup(self, app_name):
        """팝업 창으로 앱 실행 (비모달 - 동시에 여러 개 가능)"""
        dialog = QDialog(self)
        dialog.setWindowTitle(app_name)
        dialog.setGeometry(200, 200, 600, 480)
        dialog.setWindowFlags(dialog.windowFlags() | Qt.Window)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)
        app_widget = self.apps[app_name][0]()
        container = AppContainer(app_widget)
        layout.addWidget(container)

        dialog.finished.connect(lambda: self._popups.discard(dialog))
        self._popups.add(dialog)
        dialog.show()

def main():
    app = QApplication(sys.argv)

    # Windows 작업 표시줄 아이콘 인식을 위한 AppUserModelID 설정
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AppDrawer.Heart.1")
    except Exception:
        pass

    heart_icon = make_heart_icon()
    app.setWindowIcon(heart_icon)
    window = MainWindow()
    window.setWindowIcon(heart_icon)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
