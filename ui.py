import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QTextEdit, QLineEdit,
                            QLabel, QComboBox, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QFont

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        
        self.title = QLabel("Dave")
        self.title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.title)
        
        layout.addStretch()
        
        self.minimize_btn = QPushButton("—")
        self.maximize_btn = QPushButton("□")
        self.close_btn = QPushButton("×")
        
        for btn in [self.minimize_btn, self.maximize_btn, self.close_btn]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: transparent;
                    color: white;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #404040;
                }
                QPushButton#close_btn:hover {
                    background-color: #e81123;
                }
            """)
            layout.addWidget(btn)
        
        self.close_btn.setObjectName("close_btn")
        self.close_btn.clicked.connect(self.parent.close)
        self.minimize_btn.clicked.connect(self.parent.showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        
        self.old_pos = None
        
    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.parent.move(self.parent.pos() + delta)
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

class RoundedFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-radius: 10px;
            }
        """)

class ThemeManager:
    def __init__(self):
        self.themes = {}
        self.current_theme = "default"
        self.load_themes()
    
    def load_themes(self):
        themes_dir = "themes"
        if not os.path.exists(themes_dir):
            os.makedirs(themes_dir)
            self.create_default_themes()
        
        for theme_file in os.listdir(themes_dir):
            if theme_file.endswith('.json'):
                with open(os.path.join(themes_dir, theme_file), 'r', encoding='utf-8') as f:
                    theme_name = theme_file[:-5]
                    self.themes[theme_name] = json.load(f)
    
    def create_default_themes(self):
        default_theme = {
            "light": {
                "window_bg": "#ffffff",
                "title_bar_bg": "#f0f0f0",
                "text_color": "#000000",
                "accent_color": "#007acc",
                "border_radius": "10px"
            },
            "dark": {
                "window_bg": "#2b2b2b",
                "title_bar_bg": "#1e1e1e",
                "text_color": "#ffffff",
                "accent_color": "#007acc",
                "border_radius": "10px"
            }
        }
        
        with open("themes/default.json", 'w', encoding='utf-8') as f:
            json.dump(default_theme, f, indent=4)
    
    def get_theme(self, theme_name, mode="dark"):
        if theme_name in self.themes:
            return self.themes[theme_name].get(mode, self.themes[theme_name]["dark"])
        return self.themes["default"][mode]

class RoundedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.theme_manager = ThemeManager()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.container = QWidget()
        self.container.setObjectName("container")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        
        close_btn = QPushButton("×")
        close_btn.setObjectName("closeButton")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_layout.addWidget(close_btn)
        container_layout.addLayout(close_layout)
        
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        settings_panel = QWidget()
        settings_panel.setFixedWidth(200)
        settings_layout = QVBoxLayout(settings_panel)
        
        theme_label = QLabel("Тема:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.themes.keys())
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Темный", "Светлый"])
        self.mode_combo.currentTextChanged.connect(self.change_mode)
        
        settings_layout.addWidget(theme_label)
        settings_layout.addWidget(self.theme_combo)
        settings_layout.addWidget(self.mode_combo)
        settings_layout.addStretch()
        
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.send_button = QPushButton("Отправить")
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        chat_layout.addWidget(self.chat_area)
        chat_layout.addLayout(input_layout)
        
        content_layout.addWidget(settings_panel)
        content_layout.addWidget(chat_widget)
        
        container_layout.addWidget(content_widget)
        
        main_layout.addWidget(self.container)
        
        self.setMinimumSize(800, 600)
        
        self.apply_theme("default", "dark")
        
        self.old_pos = None
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None
    
    def change_theme(self, theme_name):
        self.apply_theme(theme_name, "dark" if self.mode_combo.currentText() == "Темный" else "light")
    
    def change_mode(self, mode):
        self.apply_theme(self.theme_combo.currentText(), "dark" if mode == "Темный" else "light")
    
    def apply_theme(self, theme_name, mode):
        theme = self.theme_manager.get_theme(theme_name, mode)
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: transparent;
            }}
            #container {{
                background-color: {theme['window_bg']};
                border-radius: 10px;
            }}
            QWidget {{
                color: {theme['text_color']};
            }}
            QTextEdit, QLineEdit {{
                background-color: {theme['window_bg']};
                color: {theme['text_color']};
                border: 1px solid {theme['accent_color']};
                border-radius: {theme['border_radius']};
                padding: 5px;
            }}
            QPushButton {{
                background-color: {theme['accent_color']};
                color: white;
                border: none;
                border-radius: {theme['border_radius']};
                padding: 5px 15px;
            }}
            QPushButton:hover {{
                background-color: {theme['accent_color']}dd;
            }}
            #closeButton {{
                background-color: transparent;
                color: {theme['text_color']};
                font-size: 20px;
                font-weight: bold;
            }}
            #closeButton:hover {{
                background-color: #e81123;
                color: white;
            }}
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RoundedWindow()
    window.show()
    sys.exit(app.exec_()) 