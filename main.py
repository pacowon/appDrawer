import sys
import os
import json
import subprocess
import hashlib
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFrame,
                             QScrollArea, QGridLayout, QDialog, QStackedWidget,
                             QTabWidget, QTabBar, QGroupBox, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView,
                             QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData
from PyQt5.QtGui import QFont, QDrag, QPixmap, QPainter, QColor
from PyQt5.uic import loadUi

from Apps.path_bar import PathBar
from icon import make_heart_icon
from appSetting import APP_REGISTRY, THEMES

# ── 앱 순서 영속화 ──────────────────────────────────────────
ORDER_FILE = os.path.join(os.path.expanduser("~"), "mxby", ".appdrawer_order.json")
THEME_FILE = os.path.join(os.path.expanduser("~"), "mxby", ".appdrawer_theme.json")
USAGE_FILE = os.path.join(os.path.expanduser("~"), "mxby", ".appdrawer_usage.json")
GROUPS_FILE = os.path.join(os.path.expanduser("~"), "mxby", ".appdrawer_groups.json")
GROUP_ASSIGNMENTS_FILE = os.path.join(os.path.expanduser("~"), "mxby", ".appdrawer_group_assignments.json")
MAX_USAGE_HISTORY = 500

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


def save_theme(theme_name):
    try:
        os.makedirs(os.path.dirname(THEME_FILE), exist_ok=True)
        with open(THEME_FILE, "w", encoding="utf-8") as f:
            json.dump({"theme": theme_name}, f, ensure_ascii=False)
    except Exception as e:
        print(f"[save_theme error] {e}")


def load_theme():
    if not os.path.exists(THEME_FILE):
        return "light"
    try:
        with open(THEME_FILE, "r", encoding="utf-8") as f:
            theme_name = json.load(f).get("theme", "light")
        if theme_name == "forest":
            return "pink"
        return theme_name if theme_name in THEMES else "light"
    except Exception:
        return "light"


def app_color(app_name):
    colors = [
        "#e74c3c", "#e67e22", "#f39c12", "#f1c40f", "#d4ac0d",
        "#2ecc71", "#27ae60", "#16a085", "#1abc9c", "#48c9b0",
        "#3498db", "#2e86c1", "#2980b9", "#5dade2", "#85c1e9",
        "#9b59b6", "#8e44ad", "#af7ac5", "#c39bd3", "#7d3c98",
        "#e91e63", "#d81b60", "#ec407a", "#f06292", "#ad1457",
        "#ff5722", "#f4511e", "#ff7043", "#ff8a65", "#d84315",
        "#795548", "#8d6e63", "#6d4c41", "#a1887f", "#5d4037",
        "#607d8b", "#78909c", "#546e7a", "#90a4ae", "#455a64",
        "#00bcd4", "#26c6da", "#00acc1", "#4dd0e1", "#0097a7",
        "#7cb342", "#9ccc65", "#558b2f", "#c0ca33", "#689f38",
    ]
    digest = hashlib.md5(app_name.encode("utf-8")).digest()
    return colors[digest[0] % len(colors)]


def load_usage_data():
    default_data = {"history": [], "totals": {}}
    if not os.path.exists(USAGE_FILE):
        return default_data
    try:
        with open(USAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        history = data.get("history", [])
        totals = data.get("totals", {})
        if not isinstance(history, list) or not isinstance(totals, dict):
            return default_data
        return {
            "history": history[-MAX_USAGE_HISTORY:],
            "totals": totals,
        }
    except Exception:
        return default_data


def save_usage_data(data):
    try:
        os.makedirs(os.path.dirname(USAGE_FILE), exist_ok=True)
        with open(USAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[save_usage_data error] {e}")


def record_app_usage(app_name, launch_mode):
    data = load_usage_data()
    data["history"].append(
        {
            "app": app_name,
            "mode": launch_mode,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
    )
    data["history"] = data["history"][-MAX_USAGE_HISTORY:]
    data["totals"][app_name] = int(data["totals"].get(app_name, 0)) + 1
    save_usage_data(data)


def sanitize_group_names(names):
    cleaned = []
    seen = set()
    for index, name in enumerate(names):
        text = str(name).strip() or f"GROUP {index + 1}"
        base = text
        suffix = 2
        while text in seen:
            text = f"{base} {suffix}"
            suffix += 1
        seen.add(text)
        cleaned.append(text)
    return cleaned


def _default_group_names():
    return ["GROUP 1"]


def _default_group_assignments(app_names):
    return {app_name: 0 for app_name in app_names}


def ensure_group_files(app_names):
    os.makedirs(os.path.dirname(GROUPS_FILE), exist_ok=True)
    if not os.path.exists(GROUPS_FILE):
        save_group_names(_default_group_names())
    if not os.path.exists(GROUP_ASSIGNMENTS_FILE):
        save_group_assignments(_default_group_assignments(app_names))


def load_group_names():
    if not os.path.exists(GROUPS_FILE):
        return _default_group_names()
    try:
        with open(GROUPS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        names = data.get("groups", _default_group_names())
        if not isinstance(names, list) or not names:
            return _default_group_names()
        return sanitize_group_names(names)
    except Exception:
        return _default_group_names()


def save_group_names(group_names):
    try:
        os.makedirs(os.path.dirname(GROUPS_FILE), exist_ok=True)
        with open(GROUPS_FILE, "w", encoding="utf-8") as f:
            json.dump({"groups": sanitize_group_names(group_names)}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[save_group_names error] {e}")


def load_group_assignments(app_names):
    default_assignments = _default_group_assignments(app_names)
    if not os.path.exists(GROUP_ASSIGNMENTS_FILE):
        return dict(default_assignments)
    try:
        with open(GROUP_ASSIGNMENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        saved = data.get("assignments", {})
        if not isinstance(saved, dict):
            return dict(default_assignments)
        merged = dict(default_assignments)
        for app_name, group_index in saved.items():
            if app_name in merged:
                try:
                    merged[app_name] = max(0, int(group_index))
                except Exception:
                    pass
        return merged
    except Exception:
        return dict(default_assignments)


def save_group_assignments(assignments):
    try:
        os.makedirs(os.path.dirname(GROUP_ASSIGNMENTS_FILE), exist_ok=True)
        with open(GROUP_ASSIGNMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump({"assignments": assignments}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[save_group_assignments error] {e}")


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
        self.theme_name = "light"
        self._setup_ui()

    def _setup_ui(self):
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setFixedSize(130, 130)
        self.setCursor(Qt.PointingHandCursor)
        self.setAcceptDrops(False)

        bg = app_color(self.app_name)

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
        colors = THEMES[self.theme_name]
        if dragging:
            self.setStyleSheet(
                f"AppCard{{background-color:{colors['panel_alt_bg']};"
                f"border-radius:10px;border:2px dashed {colors['accent']};}}"
            )
        else:
            self.setStyleSheet(
                f"AppCard{{background-color:{colors['card_bg']};"
                f"border-radius:10px;border:2px solid {colors['card_border']};"
                f"color:{colors['text']};}}"
                f"AppCard:hover{{background-color:{colors['card_hover_bg']};"
                f"border:2px solid {colors['card_hover_border']};}}"
            )

    def set_theme(self, theme_name):
        self.theme_name = theme_name if theme_name in THEMES else "light"
        self._apply_style(False)

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
    def __init__(self, apps, app_group_assignments, group_names, on_click, on_right_click):
        super().__init__()
        self.apps = apps
        self.app_group_assignments = app_group_assignments
        self.group_names = group_names
        self.app_order = load_order(list(apps.keys()))
        self.on_click = on_click
        self.on_right_click = on_right_click
        self.theme_name = "light"
        self.cards = []
        self.group_labels = []
        self.group_sections = []
        self.section_widgets = []
        self.setAcceptDrops(True)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(22)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.rebuild_grid()

    def rebuild_grid(self):
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.cards = []
        self.group_labels = []
        self.group_sections = []
        self.section_widgets = []
        cols = 5

        for group_index, group_name in enumerate(self.group_names):
            last_index = len(self.group_names) - 1
            group_apps = [
                name for name in self.app_order
                if min(self.app_group_assignments.get(name, last_index), last_index) == group_index
            ]

            header = QLabel(group_name)
            header.setObjectName("group_header")
            header.setFont(QFont("Arial", 16, QFont.Bold))
            self.group_labels.append(header)
            self.group_sections.append((group_index, header))
            self.main_layout.addWidget(header)

            section = QWidget()
            section.setObjectName("group_section")
            self.section_widgets.append(section)
            section_layout = QGridLayout(section)
            section_layout.setHorizontalSpacing(20)
            section_layout.setVerticalSpacing(16)
            section_layout.setContentsMargins(0, 0, 0, 0)

            for i, name in enumerate(group_apps):
                cls, icon = self.apps[name]
                card = AppCard(name, cls, icon)
                card.clicked.connect(self.on_click)
                card.rightClicked.connect(self.on_right_click)
                self.cards.append(card)
                section_layout.addWidget(card, i // cols, i % cols)

            rows = (len(group_apps) + cols - 1) // cols if group_apps else 0
            section_layout.setRowStretch(rows, 1)
            self.group_sections.append((group_index, section))
            self.main_layout.addWidget(section)

        self.main_layout.addStretch()
        self.set_theme(self.theme_name)

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
        source = self.app_order.index(dragged)
        target_group = self._get_target_group_index(event.pos())
        target_card = self._get_target_card_name(event.pos(), target_group, dragged)

        self.app_order.pop(source)
        self.app_group_assignments[dragged] = target_group

        if target_card:
            target_index = self.app_order.index(target_card)
            self.app_order.insert(target_index, dragged)
        else:
            self.app_order.insert(self._group_insert_index(target_group), dragged)

        self.rebuild_grid()
        save_order(self.app_order)
        save_group_assignments(self.app_group_assignments)
        event.acceptProposedAction()

    def _effective_group_index(self, app_name):
        last_index = len(self.group_names) - 1
        return min(self.app_group_assignments.get(app_name, last_index), last_index)

    def _widget_rect_in_self(self, widget):
        top_left = widget.mapTo(self, widget.rect().topLeft())
        return widget.geometry().translated(top_left - widget.geometry().topLeft())

    def _get_target_group_index(self, pos):
        for group_index, widget in self.group_sections:
            rect = self._widget_rect_in_self(widget)
            if rect.adjusted(-6, -6, 6, 6).contains(pos):
                return group_index

        best_group = len(self.group_names) - 1
        best_distance = float("inf")
        for group_index, widget in self.group_sections:
            center = widget.mapTo(self, widget.rect().center())
            distance = (center - pos).manhattanLength()
            if distance < best_distance:
                best_distance = distance
                best_group = group_index
        return best_group

    def _get_target_card_name(self, pos, group_index, dragged_name):
        best_name = None
        best_distance = float("inf")
        for card in self.cards:
            if card.app_name == dragged_name:
                continue
            if self._effective_group_index(card.app_name) != group_index:
                continue
            center = card.mapTo(self, card.rect().center())
            distance = (center - pos).manhattanLength()
            if distance < best_distance:
                best_distance = distance
                best_name = card.app_name
        return best_name

    def _group_insert_index(self, group_index):
        last_match = -1
        for index, app_name in enumerate(self.app_order):
            if self._effective_group_index(app_name) == group_index:
                last_match = index
        if last_match != -1:
            return last_match + 1

        for index, app_name in enumerate(self.app_order):
            if self._effective_group_index(app_name) > group_index:
                return index
        return len(self.app_order)

    def set_theme(self, theme_name):
        self.theme_name = theme_name if theme_name in THEMES else "light"
        colors = THEMES[self.theme_name]
        self.setStyleSheet(f"""
            AppGrid {{
                background-color: {colors['page_bg']};
            }}
            QWidget#group_section {{
                background-color: {colors['page_bg']};
                border: none;
            }}
        """)
        for card in self.cards:
            card.set_theme(self.theme_name)
        for label in self.group_labels:
            label.setStyleSheet(
                f"color: {colors['text']};"
                f"padding: 4px 2px 8px 2px;"
                f"border-bottom: 1px solid {colors['border']};"
            )

    def update_groups(self, group_names):
        self.group_names = sanitize_group_names(group_names)
        self.rebuild_grid()


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
        ensure_group_files(self.apps.keys())
        self.app_group_assignments = load_group_assignments(self.apps.keys())
        self.group_names = load_group_names()
        self.applied_group_names = list(self.group_names)
        self.setup_ui()

    def setup_ui(self):
        self.sidebar_expanded = True
        self.current_theme_name = load_theme()
        self.btn_apps.clicked.connect(self.show_apps)
        self.btn_settings.clicked.connect(self.show_settings)
        self.btn_profile.clicked.connect(self.show_profile)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        self.setup_apps_tabs()
        self.setup_settings_page()
        self.setup_profile_page()
        self.btn_apps.setChecked(True)
        self.content_stack.setCurrentWidget(self.apps_page)
        self.toggle_sidebar()
        self.apply_theme(self.current_theme_name)

    def setup_settings_page(self):
        while self.settings_layout.count():
            item = self.settings_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.settings_layout.setContentsMargins(40, 40, 40, 40)
        self.settings_layout.setSpacing(0)

        panel = QGroupBox("Theme")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 26, 20, 20)
        panel_layout.setSpacing(0)

        self.theme_buttons = {}
        button_row = QHBoxLayout()
        button_row.setSpacing(12)
        for theme_name, colors in THEMES.items():
            button = QPushButton(colors["label"])
            button.setCheckable(True)
            button.clicked.connect(lambda checked=False, name=theme_name: self.on_theme_button_clicked(name))
            self.theme_buttons[theme_name] = button
            button_row.addWidget(button)
        panel_layout.addLayout(button_row)

        self.settings_layout.addStretch()
        self.settings_layout.addWidget(panel)
        self.settings_layout.addSpacing(18)
        self.settings_layout.addWidget(self._build_groups_panel())
        self.settings_layout.addStretch()
        self.settings_panel = panel

    def _build_groups_panel(self):
        panel = QGroupBox("Groups")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 26, 20, 20)
        layout.setSpacing(12)

        self.group_name_inputs = []
        self.groups_rows_container = QWidget()
        self.groups_rows_layout = QVBoxLayout(self.groups_rows_container)
        self.groups_rows_layout.setContentsMargins(0, 0, 0, 0)
        self.groups_rows_layout.setSpacing(10)

        controls = QHBoxLayout()
        controls.setSpacing(10)
        self.add_group_btn = QPushButton("+ Group")
        self.remove_group_btn = QPushButton("- Group")
        self.apply_groups_btn = QPushButton("Apply")
        self.add_group_btn.clicked.connect(self.add_group_field)
        self.remove_group_btn.clicked.connect(self.remove_group_field)
        self.apply_groups_btn.clicked.connect(self.apply_group_settings)
        controls.addWidget(self.add_group_btn)
        controls.addWidget(self.remove_group_btn)
        controls.addStretch()
        controls.addWidget(self.apply_groups_btn)

        layout.addWidget(self.groups_rows_container)
        layout.addLayout(controls)

        self.groups_panel = panel
        self.rebuild_group_fields()
        return panel

    def rebuild_group_fields(self):
        while self.groups_rows_layout.count():
            item = self.groups_rows_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.group_name_inputs = []
        for index, group_name in enumerate(self.group_names):
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(10)
            index_label = QLabel(str(index + 1))
            index_label.setFixedWidth(18)
            input_field = QLineEdit(group_name)
            input_field.setPlaceholderText(f"GROUP {index + 1}")
            self.group_name_inputs.append(input_field)
            row_layout.addWidget(index_label)
            row_layout.addWidget(input_field, 1)
            self.groups_rows_layout.addWidget(row)

        if hasattr(self, "remove_group_btn"):
            self.remove_group_btn.setEnabled(len(self.group_name_inputs) > 1)

    def _group_names_from_inputs(self):
        if not hasattr(self, "group_name_inputs") or not self.group_name_inputs:
            return list(self.group_names)
        return [field.text() for field in self.group_name_inputs]

    def add_group_field(self):
        if len(self.group_names) >= 8:
            return
        self.group_names = sanitize_group_names(self._group_names_from_inputs())
        self.group_names.append(f"GROUP {len(self.group_names) + 1}")
        self.rebuild_group_fields()
        self.apply_theme(self.current_theme_name)

    def remove_group_field(self):
        if len(self.group_names) <= 1:
            return
        self.group_names = sanitize_group_names(self._group_names_from_inputs())
        self.group_names.pop()
        self.rebuild_group_fields()
        self.apply_theme(self.current_theme_name)

    def apply_group_settings(self):
        old_last_index = len(self.applied_group_names) - 1
        group_names = sanitize_group_names(self._group_names_from_inputs())
        clamp_index = min(old_last_index, len(group_names) - 1)
        for app_name in list(self.app_group_assignments.keys()):
            self.app_group_assignments[app_name] = min(
                int(self.app_group_assignments.get(app_name, clamp_index)),
                clamp_index,
            )
        self.group_names = group_names
        self.applied_group_names = list(group_names)
        save_group_names(group_names)
        save_group_assignments(self.app_group_assignments)
        for grid in self.findChildren(AppGrid):
            grid.update_groups(group_names)
        self.rebuild_group_fields()
        self.apply_theme(self.current_theme_name)

    def on_theme_button_clicked(self, theme_name):
        self.apply_theme(theme_name)
        save_theme(theme_name)

    def setup_profile_page(self):
        while self.profile_layout.count():
            item = self.profile_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.profile_layout.setContentsMargins(40, 40, 40, 40)
        self.profile_layout.setSpacing(0)

        panel = QGroupBox("Usage Ranking")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(18, 26, 18, 18)
        panel_layout.setSpacing(14)

        self.profile_summary_label = QLabel()

        self.profile_table = QTableWidget(0, 3)
        self.profile_table.setHorizontalHeaderLabels(["Rank", "App", "Count"])
        self.profile_table.verticalHeader().setVisible(False)
        self.profile_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.profile_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.profile_table.setFocusPolicy(Qt.NoFocus)
        self.profile_table.setShowGrid(False)
        self.profile_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.profile_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.profile_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        panel_layout.addWidget(self.profile_summary_label)
        panel_layout.addWidget(self.profile_table)

        self.profile_layout.addStretch()
        self.profile_layout.addWidget(panel)
        self.profile_layout.addStretch()

        self.profile_panel = panel
        self.refresh_profile_page()

    def refresh_profile_page(self):
        if not hasattr(self, "profile_table"):
            return

        usage_data = load_usage_data()
        totals = usage_data["totals"]
        ranking = sorted(totals.items(), key=lambda item: (-item[1], item[0]))

        self.profile_table.setRowCount(len(ranking))
        for row, (app_name, count) in enumerate(ranking):
            rank_item = QTableWidgetItem(str(row + 1))
            app_item = QTableWidgetItem(app_name)
            count_item = QTableWidgetItem(str(count))
            rank_item.setTextAlignment(Qt.AlignCenter)
            count_item.setTextAlignment(Qt.AlignCenter)
            self.profile_table.setItem(row, 0, rank_item)
            self.profile_table.setItem(row, 1, app_item)
            self.profile_table.setItem(row, 2, count_item)

        total_launches = sum(int(value) for value in totals.values())
        history_count = len(usage_data["history"])
        if ranking:
            top_app, top_count = ranking[0]
            self.profile_summary_label.setText(
                f"Total {total_launches} launches  |  History {history_count}/{MAX_USAGE_HISTORY}  |  #1 {top_app} ({top_count})"
            )
        else:
            self.profile_summary_label.setText(
                f"Total 0 launches  |  History 0/{MAX_USAGE_HISTORY}"
            )

    def apply_theme(self, theme_name):
        self.current_theme_name = theme_name if theme_name in THEMES else "light"
        colors = THEMES[self.current_theme_name]

        self.setStyleSheet(f"""
            QMainWindow, QWidget#centralwidget {{
                background-color: {colors['window_bg']};
                color: {colors['text']};
            }}
            QWidget#apps_page, QWidget#settings_page, QWidget#profile_page {{
                background-color: {colors['page_bg']};
                color: {colors['text']};
            }}
            QLabel {{
                color: {colors['text']};
            }}
            QFrame {{
                color: {colors['text']};
            }}
            QScrollArea {{
                border: none;
                background-color: {colors['page_bg']};
            }}
            QTabWidget::pane {{
                border: 1px solid {colors['border']};
                background: {colors['panel_bg']};
            }}
            QTabBar::tab {{
                background: {colors['panel_alt_bg']};
                color: {colors['text']};
                padding: 10px 20px;
                margin-right: 2px;
                border: 1px solid {colors['border']};
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }}
            QTabBar::tab:selected {{
                background: {colors['panel_bg']};
            }}
            QTabBar::tab:hover {{
                background: {colors['card_hover_bg']};
            }}
        """)

        if hasattr(self, "apps_tab_widget"):
            self.apps_tab_widget.setStyleSheet(f"""
                QTabWidget::pane {{
                    border: 1px solid {colors['border']};
                    background: {colors['panel_bg']};
                }}
                QTabBar::tab {{
                    background: {colors['panel_alt_bg']};
                    color: {colors['text']};
                    padding: 10px 20px;
                    margin-right: 2px;
                    border: 1px solid {colors['border']};
                    border-bottom: none;
                    border-top-left-radius: 5px;
                    border-top-right-radius: 5px;
                }}
                QTabBar::tab:selected {{
                    background: {colors['panel_bg']};
                    color: {colors['text']};
                    border-bottom: 1px solid {colors['panel_bg']};
                }}
                QTabBar::tab:hover {{
                    background: {colors['card_hover_bg']};
                    color: {colors['text']};
                }}
            """)

        self.sidebar.setStyleSheet(f"background-color: {colors['sidebar_bg']};")
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['sidebar_bg']};
                color: {colors['sidebar_text']};
                border: none;
                font-size: 20px;
            }}
            QPushButton:hover {{
                background-color: {colors['sidebar_hover']};
            }}
        """)
        sidebar_button_style = f"""
            QPushButton {{
                text-align: left;
                padding: 15px;
                border: none;
                background-color: transparent;
                color: {colors['sidebar_text']};
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {colors['sidebar_hover']};
            }}
            QPushButton:checked {{
                background-color: {colors['sidebar_checked']};
            }}
        """
        self.btn_apps.setStyleSheet(sidebar_button_style)
        self.btn_settings.setStyleSheet(sidebar_button_style)
        self.btn_profile.setStyleSheet(sidebar_button_style)

        if hasattr(self, "settings_panel"):
            self.settings_panel.setStyleSheet(f"""
                QGroupBox {{
                    background-color: {colors['panel_bg']};
                    border: 1px solid {colors['border']};
                    border-radius: 14px;
                    color: {colors['text']};
                    font-size: 15px;
                    font-weight: bold;
                    padding-top: 12px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 18px;
                    top: 10px;
                    padding: 0 8px;
                    background-color: {colors['panel_bg']};
                }}
            """)
        if hasattr(self, "groups_panel"):
            self.groups_panel.setStyleSheet(f"""
                QGroupBox {{
                    background-color: {colors['panel_bg']};
                    border: 1px solid {colors['border']};
                    border-radius: 14px;
                    color: {colors['text']};
                    font-size: 15px;
                    font-weight: bold;
                    padding-top: 12px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 18px;
                    top: 10px;
                    padding: 0 8px;
                    background-color: {colors['panel_bg']};
                }}
                QLineEdit {{
                    background-color: {colors['input_bg']};
                    color: {colors['text']};
                    border: 1px solid {colors['border']};
                    border-radius: 8px;
                    padding: 8px 10px;
                }}
            """)
        for button_name in ["add_group_btn", "remove_group_btn", "apply_groups_btn"]:
            if hasattr(self, button_name):
                button = getattr(self, button_name)
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {colors['panel_alt_bg'] if button_name != 'apply_groups_btn' else colors['accent']};
                        color: {colors['text'] if button_name != 'apply_groups_btn' else '#ffffff'};
                        border: 1px solid {colors['border'] if button_name != 'apply_groups_btn' else colors['accent']};
                        border-radius: 10px;
                        padding: 10px 14px;
                        font-size: 12px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: {colors['card_hover_bg'] if button_name != 'apply_groups_btn' else colors['accent_hover']};
                    }}
                    QPushButton:disabled {{
                        color: {colors['muted_text']};
                    }}
                """)
        if hasattr(self, "profile_panel"):
            self.profile_panel.setStyleSheet(f"""
                QGroupBox {{
                    background-color: {colors['panel_bg']};
                    border: 1px solid {colors['border']};
                    border-radius: 14px;
                    color: {colors['text']};
                    font-size: 15px;
                    font-weight: bold;
                    padding-top: 12px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 18px;
                    top: 10px;
                    padding: 0 8px;
                    background-color: {colors['panel_bg']};
                }}
            """)
        if hasattr(self, "profile_summary_label"):
            self.profile_summary_label.setStyleSheet(
                f"color: {colors['muted_text']}; font-size: 12px; padding: 0 2px 4px 2px;"
            )
        if hasattr(self, "profile_table"):
            self.profile_table.setStyleSheet(f"""
                QTableWidget {{
                    background-color: {colors['panel_bg']};
                    color: {colors['text']};
                    border: none;
                    gridline-color: {colors['border']};
                    outline: 0;
                }}
                QHeaderView::section {{
                    background-color: {colors['panel_alt_bg']};
                    color: {colors['text']};
                    border: none;
                    border-bottom: 1px solid {colors['border']};
                    padding: 8px;
                    font-weight: bold;
                }}
                QTableWidget::item {{
                    padding: 8px;
                    border-bottom: 1px solid {colors['border']};
                }}
            """)
        if hasattr(self, "theme_buttons"):
            for theme_name, button in self.theme_buttons.items():
                is_active = theme_name == self.current_theme_name
                button.setChecked(is_active)
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {colors['accent'] if is_active else colors['panel_alt_bg']};
                        color: {"#ffffff" if is_active else colors['text']};
                        border: 1px solid {colors['accent'] if is_active else colors['border']};
                        border-radius: 10px;
                        padding: 12px 18px;
                        font-size: 13px;
                        font-weight: bold;
                        min-width: 88px;
                    }}
                    QPushButton:hover {{
                        background-color: {colors['accent_hover'] if is_active else colors['card_hover_bg']};
                    }}
                """)

        self._apply_theme_to_dynamic_widgets()

    def _apply_theme_to_dynamic_widgets(self):
        colors = THEMES[self.current_theme_name]

        for card in self.findChildren(AppCard):
            card.set_theme(self.current_theme_name)

        for grid in self.findChildren(AppGrid):
            grid.set_theme(self.current_theme_name)

        for path_bar in self._tab_path_bars.values():
            if isinstance(path_bar, PathBar):
                path_bar.apply_theme(colors, disabled=not path_bar.isEnabled())

    def setup_apps_tabs(self):
        while self.apps_page_layout.count():
            child = self.apps_page_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.apps_tab_widget = QTabWidget()
        self.apps_tab_widget.setTabsClosable(True)
        self.apps_tab_widget.tabCloseRequested.connect(self.close_app_tab)
        self._tab_path_bars = {}         # {id(tab_stack): PathBar}
        self._stack_to_container = {}    # {id(tab_stack): tab_container}
        self.add_new_app_tab("App List 1")
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
        tab_container.setObjectName("app_tab_container")
        container_layout = QVBoxLayout(tab_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        tab_stack = QStackedWidget()
        tab_stack.setObjectName("app_tab_stack")
        grid_page = QWidget()
        grid_page.setObjectName("app_grid_page")
        grid_layout = QVBoxLayout(grid_page)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setObjectName("app_grid_scroll")
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")
        app_grid = AppGrid(
            self.apps,
            self.app_group_assignments,
            self.group_names,
            on_click=lambda name, s=tab_stack, t=tab_name: self.launch_app_in_tab(name, s, t),
            on_right_click=self.launch_app_popup
        )
        app_grid.set_theme(self.current_theme_name)
        scroll.setWidget(app_grid)
        grid_layout.addWidget(scroll)
        tab_stack.addWidget(grid_page)

        # 탭별 PathBar
        path_bar = PathBar()
        self._tab_path_bars[id(tab_stack)] = path_bar
        self._tab_path_bars[id(tab_container)] = path_bar   # container로도 조회 가능
        # tab_stack → tab_container 역방향 매핑 (탭 인덱스 조회용)
        self._stack_to_container[id(tab_stack)] = tab_container
        path_bar.apply_theme(THEMES[self.current_theme_name], disabled=False)
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
        record_app_usage(app_name, "tab")
        app_page = QWidget()
        app_layout = QVBoxLayout(app_page)
        app_layout.setContentsMargins(0, 0, 0, 0)

        # 해당 탭의 PathBar 비활성화 + 시각적 표시
        path_bar = self._tab_path_bars.get(id(tab_stack))
        if path_bar:
            path_bar.apply_theme(THEMES[self.current_theme_name], disabled=True)

        def go_back():
            tab_stack.setCurrentIndex(0)
            idx = self.apps_tab_widget.indexOf(tab_container) if tab_container else -1
            if idx >= 0:
                self.apps_tab_widget.setTabText(idx, original_tab_name)
            # PathBar 원래 스타일로 복원
            if path_bar:
                path_bar.apply_theme(THEMES[self.current_theme_name], disabled=False)

        back_btn = QPushButton("← Return to Menu")
        back_btn.clicked.connect(go_back)
        colors = THEMES[self.current_theme_name]
        back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['accent']};
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {colors['accent_hover']};
            }}
        """)
        target_path = self._get_tab_path(tab_stack)
        previous_cwd = os.getcwd()
        try:
            os.chdir(target_path)
            app_widget = self.apps[app_name][0]()
        finally:
            os.chdir(previous_cwd)

        if hasattr(app_widget, "set_path_provider"):
            app_widget.set_path_provider(lambda s=tab_stack: self._get_tab_path(s))

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
            self.add_new_app_tab(f"App List {n + 1}")

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
        self.refresh_profile_page()
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
        record_app_usage(app_name, "popup")
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
