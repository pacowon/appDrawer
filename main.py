import sys
import os
import json
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFrame,
                             QScrollArea, QGridLayout, QDialog, QStackedWidget,
                             QTabWidget, QTabBar)
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData
from PyQt5.QtGui import QFont, QDrag, QPixmap, QPainter, QColor
from PyQt5.uic import loadUi

from Apps.path_bar import PathBar
from icon import make_heart_icon
from appSetting import APP_REGISTRY

# ── 앱 순서 영속화 ──────────────────────────────────────────
ORDER_FILE = os.path.join(os.path.expanduser("~"), "mxby", ".appdrawer_order.json")

def save_order(order):
    try:
        os.makedirs(os.path.dirname(ORDER_FILE), exist_ok=True)
        with open(ORDER_FILE, "w", encoding="utf-8") as f:
            json.dump(order, f, ensure_ascii=False)
    except Exception as e:
        print(f"[save_order error] {e}")

def load_order(default_keys):
    if not os.path.exists(ORDER_FILE):
        return list(default_keys)
    try:
        with open(ORDER_FILE, "r", encoding="utf-8") as f:
            saved = json.load(f)
        valid   = [k for k in saved if k in default_keys]
        new     = [k for k in default_keys if k not in valid]
        return valid + new
    except Exception:
        return list(default_keys)


# ── 앱 카드 ────────────────────────────────────────────────
class AppCard(QFrame):
    clicked = pyqtSignal(str)
    rightClicked = pyqtSignal(str)

    def __init__(self, app_name, app_class, icon="??"):
        super().__init__()
        self.app_name = app_name
        self.app_class = app_class
        self.icon = icon
        self._drag_start_pos = None
        self._setup_ui()

    def _setup_ui(self):
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setFixedSize(130, 130)
        self.setCursor(Qt.PointingHandCursor)
        self.setAcceptDrops(False)

        colors = ["#e74c3c","#e67e22","#f1c40f","#2ecc71",
                  "#1abc9c","#3498db","#2980b9","#9b59b6",
                  "#8e44ad","#e91e63","#00bcd4","#ff5722"]
        bg = colors[hash(self.app_name) % len(colors)]

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(4)

        badge = QLabel(self.icon)
        badge.setAlignment(Qt.AlignCenter)
        badge.setFixedSize(64, 64)
        badge.setFont(QFont("Arial", 20, QFont.Bold))
        badge.setStyleSheet(
            f"QLabel{{background-color:{bg};color:white;border-radius:32px;}}"
        )

        name_lbl = QLabel(self.app_name)
        name_lbl.setAlignment(Qt.AlignCenter)
        name_lbl.setFont(QFont("Arial", 10))
        name_lbl.setWordWrap(True)

        layout.addWidget(badge, 0, Qt.AlignHCenter)
        layout.addWidget(name_lbl)
        self.setLayout(layout)
        self._apply_style(False)

    def _apply_style(self, dragging):
        if dragging:
            self.setStyleSheet(
                "AppCard{background-color:#c8e6c9;border-radius:10px;border:2px dashed #4CAF50;}"
            )
        else:
            self.setStyleSheet(
                "AppCard{background-color:#f0f0f0;border-radius:10px;border:2px solid #ddd;}"
                "AppCard:hover{background-color:#e0e0e0;border:2px solid #4CAF50;}"
            )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = event.pos()
        elif event.button() == Qt.RightButton:
            self.rightClicked.emit(self.app_name)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton) or self._drag_start_pos is None:
            return
        if (event.pos() - self._drag_start_pos).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(self.app_name)
        drag.setMimeData(mime)
        px = QPixmap(self.size())
        px.fill(QColor(0, 0, 0, 0))
        p = QPainter(px)
        p.setOpacity(0.7)
        self.render(p)
        p.end()
        drag.setPixmap(px)
        drag.setHotSpot(event.pos())
        self._apply_style(True)
        drag.exec_(Qt.MoveAction)
        self._apply_style(False)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self._drag_start_pos is not None:
                if (event.pos() - self._drag_start_pos).manhattanLength() < QApplication.startDragDistance():
                    self.clicked.emit(self.app_name)
            self._drag_start_pos = None


# ── 앱 그리드 ──────────────────────────────────────────────
class AppGrid(QWidget):
    def __init__(self, apps, on_click, on_right_click):
        super().__init__()
        self.apps = apps
        self.app_order = load_order(list(apps.keys()))
        self.on_click = on_click
        self.on_right_click = on_right_click
        self.setAcceptDrops(True)
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        self.rebuild_grid()

    def rebuild_grid(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        cols = 5
        for i, name in enumerate(self.app_order):
            cls, icon = self.apps[name]
            card = AppCard(name, cls, icon)
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
        dragged = event.mimeData().text()
        target  = self._get_drop_index(event.pos())
        source  = self.app_order.index(dragged)
        if target != source and target != -1:
            self.app_order.insert(target, self.app_order.pop(source))
            self.rebuild_grid()
            save_order(self.app_order)
        event.acceptProposedAction()

    def _get_drop_index(self, pos):
        best_i, best_d = len(self.app_order) - 1, float('inf')
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                d = (item.widget().geometry().center() - pos).manhattanLength()
                if d < best_d:
                    best_d, best_i = d, i
        return best_i


# ── 사이드바 버튼 ───────────────────────────────────────────
class SidebarButton(QPushButton):
    def __init__(self, text, icon_text=""):
        super().__init__()
        self.full_text = text
        self.icon_text = icon_text
        self.setText(f"{icon_text}  {text}")
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                text-align:left; padding:15px; border:none;
                background-color:transparent; color:white; font-size:14px;
            }
            QPushButton:hover  { background-color:rgba(255,255,255,0.1); }
            QPushButton:checked{ background-color:rgba(255,255,255,0.2); }
        """)

    def update_text(self, expanded):
        self.setText(f"{self.icon_text}  {self.full_text}" if expanded else self.icon_text)


# ── 메인 윈도우 ─────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'mainwindow.ui')
        loadUi(ui_path, self)
        self.apps = APP_REGISTRY
        self._popups = set()
        self.setup_ui()

    def setup_ui(self):
        self.sidebar_expanded = True
        self.btn_apps.clicked.connect(self.show_apps)
        self.btn_settings.clicked.connect(self.show_settings)
        self.btn_profile.clicked.connect(self.show_profile)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        self.setup_apps_tabs()
        self.btn_apps.setChecked(True)
        self.content_stack.setCurrentWidget(self.apps_page)

    def setup_apps_tabs(self):
        while self.apps_page_layout.count():
            child = self.apps_page_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.apps_tab_widget = QTabWidget()
        self.apps_tab_widget.setTabsClosable(True)
        self.apps_tab_widget.tabCloseRequested.connect(self.close_app_tab)
        self.apps_tab_widget.setStyleSheet("""
            QTabWidget::pane { border:1px solid #ddd; background:white; }
            QTabBar::tab {
                background:#f0f0f0; padding:10px 20px; margin-right:2px;
                border:1px solid #ddd; border-bottom:none;
                border-top-left-radius:5px; border-top-right-radius:5px;
            }
            QTabBar::tab:selected { background:white; border-bottom:1px solid white; }
            QTabBar::tab:hover    { background:#e0e0e0; }
        """)
        self._tab_path_bars = {}         # {id(tab_stack): PathBar}
        self._stack_to_container = {}    # {id(tab_stack): tab_container}
        self.add_new_app_tab("앱 목록 1")
        plus_widget = QWidget()
        self.apps_tab_widget.addTab(plus_widget, "+")
        self.apps_tab_widget.tabBar().setTabButton(
            self.apps_tab_widget.count() - 1, QTabBar.RightSide, None)
        self.apps_tab_widget.currentChanged.connect(self.on_tab_changed)
        self.apps_page_layout.addWidget(self.apps_tab_widget)

    def _get_tab_path(self, tab_stack):
        """탭 스택에 연결된 PathBar의 경로 반환"""
        pb = self._tab_path_bars.get(id(tab_stack))
        return pb.path if pb else os.getcwd()

    def _get_active_tab_path(self):
        """현재 활성 탭의 PathBar 경로 반환 (팝업용)"""
        idx = self.apps_tab_widget.currentIndex()
        container = self.apps_tab_widget.widget(idx)
        pb = self._tab_path_bars.get(id(container))
        return pb.path if pb else os.getcwd()

    def add_new_app_tab(self, tab_name):
        # 탭 전체를 감싸는 컨테이너 (그리드 + PathBar)
        tab_container = QWidget()
        container_layout = QVBoxLayout(tab_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        tab_stack = QStackedWidget()
        grid_page = QWidget()
        grid_layout = QVBoxLayout(grid_page)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")
        app_grid = AppGrid(
            self.apps,
            on_click=lambda name, s=tab_stack, t=tab_name: self.launch_app_in_tab(name, s, t),
            on_right_click=self.launch_app_popup
        )
        scroll.setWidget(app_grid)
        grid_layout.addWidget(scroll)
        tab_stack.addWidget(grid_page)

        # 탭별 PathBar
        path_bar = PathBar()
        self._tab_path_bars[id(tab_stack)] = path_bar
        self._tab_path_bars[id(tab_container)] = path_bar   # container로도 조회 가능
        # tab_stack → tab_container 역방향 매핑 (탭 인덱스 조회용)
        self._stack_to_container[id(tab_stack)] = tab_container
        container_layout.addWidget(tab_stack, 1)
        container_layout.addWidget(path_bar)

        idx = self.apps_tab_widget.count() - 1
        self.apps_tab_widget.insertTab(idx, tab_container, tab_name)
        self.apps_tab_widget.setCurrentIndex(idx)

    def launch_app_in_tab(self, app_name, tab_stack, original_tab_name):
        # tab_container 기준으로 탭 인덱스 찾기
        tab_container = self._stack_to_container.get(id(tab_stack))
        tab_index = self.apps_tab_widget.indexOf(tab_container) if tab_container else -1
        if tab_index >= 0:
            self.apps_tab_widget.setTabText(tab_index, app_name)
        app_page = QWidget()
        app_layout = QVBoxLayout(app_page)
        app_layout.setContentsMargins(0, 0, 0, 0)

        # 해당 탭의 PathBar 비활성화 + 시각적 표시
        path_bar = self._tab_path_bars.get(id(tab_stack))
        if path_bar:
            path_bar.setEnabled(False)
            path_bar.setStyleSheet("""
                PathBar {
                    background-color: #d5d8dc;
                    border-top: 1px solid #aab7b8;
                }
            """)
            path_bar.change_btn.setStyleSheet("""
                QPushButton {
                    background-color: #aab7b8; color: #7f8c8d;
                    border: none; border-radius: 4px;
                    padding: 0 10px; font-size: 11px;
                }
            """)

        def go_back():
            tab_stack.setCurrentIndex(0)
            idx = self.apps_tab_widget.indexOf(tab_container) if tab_container else -1
            if idx >= 0:
                self.apps_tab_widget.setTabText(idx, original_tab_name)
            # PathBar 원래 스타일로 복원
            if path_bar:
                path_bar.setEnabled(True)
                path_bar.setStyleSheet("""
                    PathBar {
                        background-color: #ecf0f1;
                        border-top: 1px solid #bdc3c7;
                    }
                """)
                path_bar.change_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db; color: white;
                        border: none; border-radius: 4px;
                        padding: 0 10px; font-size: 11px;
                    }
                    QPushButton:hover { background-color: #2980b9; }
                """)

        back_btn = QPushButton("← 앱 목록으로")
        back_btn.clicked.connect(go_back)
        back_btn.setStyleSheet("""
            QPushButton { background-color:#3498db; color:white; border:none;
                          padding:10px; font-size:14px; }
            QPushButton:hover { background-color:#2980b9; }
        """)
        os.chdir(self._get_tab_path(tab_stack))
        app_widget = self.apps[app_name][0]()
        app_layout.addWidget(back_btn)
        app_layout.addWidget(app_widget, 1)
        while tab_stack.count() > 1:
            w = tab_stack.widget(1)
            tab_stack.removeWidget(w)
            w.deleteLater()
        tab_stack.addWidget(app_page)
        tab_stack.setCurrentIndex(1)

    def on_tab_changed(self, index):
        if index == self.apps_tab_widget.count() - 1:
            n = self.apps_tab_widget.count() - 1
            self.add_new_app_tab(f"앱 목록 {n + 1}")

    def close_app_tab(self, index):
        if self.apps_tab_widget.count() > 2:
            self.apps_tab_widget.removeTab(index)

    def toggle_sidebar(self):
        self.sidebar_expanded = not self.sidebar_expanded
        self.sidebar.setFixedWidth(200 if self.sidebar_expanded else 60)
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

    def closeEvent(self, event):
        event.accept()
        QApplication.instance().quit()

    def launch_app_popup(self, app_name):
        """우클릭: 완전히 독립된 별도 프로세스로 앱 실행"""
        work_dir = self._get_active_tab_path()
        launcher = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'run_app.py')
        subprocess.Popen(
            [sys.executable, launcher, app_name, work_dir],
            cwd=work_dir
        )


# ── 진입점 ──────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AppDrawer.Heart.1")
    except Exception:
        pass
    heart_icon = make_heart_icon()
    app.setWindowIcon(heart_icon)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    window.setWindowIcon(heart_icon)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
