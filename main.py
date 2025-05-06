import sys
import json
import os
from datetime import datetime
from PyQt5.QtCore import Qt, QTranslator, QLocale, QSize, QPoint, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QComboBox,
    QStackedWidget,
    QFrame,
    QSplitter,
    QFileDialog,
    QMessageBox,
    QLineEdit
)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QPainter, QPainterPath
import code
import loader
from translations import Translations


class ModernButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(35)
        self.setFont(QFont("Segoe UI", 10))


class ModernTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Segoe UI", 10))
        self.setMinimumHeight(100)


class ModernComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Segoe UI", 10))
        self.setMinimumHeight(35)
        self.setCursor(Qt.PointingHandCursor)


class ModernLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Segoe UI", 10))


class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        layout.addWidget(ModernLabel(self.tr("Language")))
        self.language_combo = ModernComboBox()
        self.language_combo.addItems(['English', 'Русский', 'Deutsch'])
        self.language_combo.setCurrentText(self.get_language_name(self.parent.settings['language']))
        self.language_combo.currentTextChanged.connect(self.change_language)
        layout.addWidget(self.language_combo)
        
        layout.addWidget(ModernLabel(self.tr("Theme")))
        self.theme_combo = ModernComboBox()
        self.theme_combo.addItems(["Default"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        layout.addWidget(self.theme_combo)
        
        layout.addWidget(ModernLabel(self.tr("Mode")))
        self.mode_combo = ModernComboBox()
        self.mode_combo.addItems([self.tr("Dark"), self.tr("Light")])
        self.mode_combo.setCurrentText(self.tr("Dark") if self.parent.settings['dark_mode'] else self.tr("Light"))
        self.mode_combo.currentTextChanged.connect(self.change_mode)
        layout.addWidget(self.mode_combo)
        
        layout.addStretch()
    
    def load_themes(self):
        themes_dir = "themes"
        if not os.path.exists(themes_dir):
            os.makedirs(themes_dir)
        
        themes = []
        for theme_file in os.listdir(themes_dir):
            if theme_file.endswith('.json'):
                themes.append(theme_file[:-5])  # убираем .json
        
        self.theme_combo.addItems(themes)
    
    def get_language_name(self, code):
        return {
            'en': 'English',
            'ru': 'Русский',
            'de': 'Deutsch'
        }.get(code, 'English')
    
    def get_language_code(self, name):
        return {
            'English': 'en',
            'Русский': 'ru',
            'Deutsch': 'de'
        }.get(name, 'en')
    
    def change_language(self, language):
        code = self.get_language_code(language)
        self.parent.settings['language'] = code
        self.parent.translations.set_language(code)
        self.parent.update_translations()
        self.parent.save_settings()
    
    def change_theme(self, theme_name):
        self.parent.apply_theme(theme_name, "dark" if self.mode_combo.currentText() == "Dark" else "light")
    
    def change_mode(self, mode):
        self.parent.settings['dark_mode'] = (mode == self.tr("Dark"))
        self.parent.apply_theme(self.theme_combo.currentText(), "dark" if mode == self.tr("Dark") else "light")
        self.parent.save_settings()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.old_pos = None
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        
        self.settings = self.load_settings()
        self.translations = Translations()
        self.translations.set_language(self.settings['language'])
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.container = QWidget()
        self.container.setObjectName("container")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        
        top_panel = QWidget()
        top_layout = QHBoxLayout(top_panel)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(5)
        
        self.settings_btn = ModernButton("⚙")
        self.settings_btn.setFixedSize(30, 30)
        self.settings_btn.clicked.connect(self.toggle_settings)
        top_layout.addWidget(self.settings_btn)
        
        top_layout.addStretch()
        
        minimize_btn = ModernButton("🗕")
        minimize_btn.setObjectName("minimizeButton")
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.clicked.connect(self.showMinimized)
        top_layout.addWidget(minimize_btn)
        
        close_btn = ModernButton("✕")
        close_btn.setObjectName("closeButton")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        top_layout.addWidget(close_btn)
        
        container_layout.addWidget(top_panel)
        
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)
        
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        
        clear_history_btn = ModernButton(self.tr("Clear History"))
        clear_history_btn.clicked.connect(self.clear_chat_history)
        chat_layout.addWidget(clear_history_btn)
        
        self.chat_area = ModernTextEdit()
        self.chat_area.setReadOnly(True)
        
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Segoe UI", 10))
        self.input_field.setMinimumHeight(35)
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_button = ModernButton(self.tr("Send"))
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        chat_layout.addWidget(self.chat_area)
        chat_layout.addLayout(input_layout)
        
        self.tab_widget = QStackedWidget()
        
        chat_tab = QWidget()
        chat_tab_layout = QVBoxLayout(chat_tab)
        chat_tab_layout.setContentsMargins(0, 0, 0, 0)
        chat_tab_layout.addWidget(chat_widget)
        self.tab_widget.addWidget(chat_tab)
        
        self.settings_tab = SettingsTab(self)
        self.tab_widget.addWidget(self.settings_tab)
        
        content_layout.addWidget(self.tab_widget)
        
        container_layout.addWidget(content_widget)
        
        main_layout.addWidget(self.container)
        
        self.setMinimumSize(800, 600)
        
        self.apply_theme("default", "dark" if self.settings['dark_mode'] else "light")
        self.load_chat_history()
        self.center_window()
    
    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)
    
    def load_settings(self):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                'language': 'en',
                'dark_mode': True
            }
    
    def save_settings(self):
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=4)
    
    def toggle_settings(self):
        if self.tab_widget.currentIndex() == 0:
            self.tab_widget.setCurrentIndex(1)
            self.settings_btn.setText("←")
        else:
            self.tab_widget.setCurrentIndex(0)
            self.settings_btn.setText("⚙")
    
    def send_message(self):
        message = self.input_field.text().strip()
        if not message:
            return
        
        self.input_field.clear()
        self.chat_area.append(f"<b>{self.tr('You')}:</b> {message}")
        
        try:
            response = code.get_ai_response(message, self.settings['language'])
            self.chat_area.append(f"<b>{self.tr('Dave')}:</b> {response}")
            self.save_chat_history()
        except Exception as e:
            self.chat_area.append(f"<b>{self.tr('Error')}:</b> {str(e)}")
    
    def save_chat_history(self):
        try:
            with open('chat_history.txt', 'w', encoding='utf-8') as f:
                f.write(self.chat_area.toPlainText())
        except:
            pass
    
    def load_chat_history(self):
        try:
            if os.path.exists('chat_history.txt'):
                with open('chat_history.txt', 'r', encoding='utf-8') as f:
                    self.chat_area.setText(f.read())
        except:
            pass
    
    def tr(self, text):
        return self.translations.get_translation(self.settings['language'], text)

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
    
    def clear_chat_history(self):
        reply = QMessageBox.question(self, self.tr("Confirmation"),
                                   self.tr("Are you sure you want to clear chat history?"),
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.chat_area.clear()
            self.save_chat_history()
    
    def apply_theme(self, theme_name, mode):
        if theme_name == "default":
            if mode == "dark":
                self.container.setStyleSheet("""
                    QWidget#container {
                        background-color: #2b2b2b;
                        border: 1px solid #3d3d3d;
                        border-radius: 10px;
                    }
                    QTextEdit {
                        background-color: #1e1e1e;
                        color: #ffffff;
                        border: 1px solid #3d3d3d;
                        border-radius: 5px;
                    }
                    QLineEdit {
                        background-color: #1e1e1e;
                        color: #ffffff;
                        border: 1px solid #3d3d3d;
                        border-radius: 5px;
                    }
                    QPushButton {
                        background-color: #0d47a1;
                        color: white;
                        border: none;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #1565c0;
                    }
                    QPushButton#closeButton {
                        background-color: #dc3545;
                    }
                    QPushButton#closeButton:hover {
                        background-color: #c82333;
                    }
                    QPushButton#minimizeButton {
                        background-color: #6c757d;
                    }
                    QPushButton#minimizeButton:hover {
                        background-color: #5a6268;
                    }
                    QComboBox {
                        background-color: #1e1e1e;
                        color: #ffffff;
                        border: 1px solid #3d3d3d;
                        border-radius: 5px;
                    }
                    QComboBox::drop-down {
                        border: none;
                    }
                    QComboBox::down-arrow {
                        image: none;
                        border: none;
                    }
                """)
            else:
                self.container.setStyleSheet("""
                    QWidget#container {
                        background-color: #ffffff;
                        border: 1px solid #e0e0e0;
                        border-radius: 10px;
                    }
                    QTextEdit {
                        background-color: #f5f5f5;
                        color: #000000;
                        border: 1px solid #e0e0e0;
                        border-radius: 5px;
                    }
                    QLineEdit {
                        background-color: #f5f5f5;
                        color: #000000;
                        border: 1px solid #e0e0e0;
                        border-radius: 5px;
                    }
                    QPushButton {
                        background-color: #0d47a1;
                        color: white;
                        border: none;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #1565c0;
                    }
                    QPushButton#closeButton {
                        background-color: #dc3545;
                    }
                    QPushButton#closeButton:hover {
                        background-color: #c82333;
                    }
                    QPushButton#minimizeButton {
                        background-color: #6c757d;
                    }
                    QPushButton#minimizeButton:hover {
                        background-color: #5a6268;
                    }
                    QComboBox {
                        background-color: #f5f5f5;
                        color: #000000;
                        border: 1px solid #e0e0e0;
                        border-radius: 5px;
                    }
                    QComboBox::drop-down {
                        border: none;
                    }
                    QComboBox::down-arrow {
                        image: none;
                        border: none;
                    }
                """)

    def update_translations(self):
        self.settings_btn.setText("⚙")
        self.send_button.setText(self.tr("Send"))
        self.settings_tab.language_combo.setCurrentText(self.get_language_name(self.settings['language']))
        self.settings_tab.mode_combo.setCurrentText(self.tr("Dark") if self.settings['dark_mode'] else self.tr("Light"))
        
        current_text = self.chat_area.toPlainText()
        if current_text:
            translations = {
                "You:": self.tr("You:"),
                "Dave:": self.tr("Dave:"),
                "Error:": self.tr("Error:"),
                "Clear History": self.tr("Clear History"),
                "Send": self.tr("Send"),
                "Confirmation": self.tr("Confirmation"),
                "Are you sure you want to clear chat history?": self.tr("Are you sure you want to clear chat history?"),
                "Yes": self.tr("Yes"),
                "No": self.tr("No")
            }
            
            for eng, translated in translations.items():
                current_text = current_text.replace(eng, translated)
            
            self.chat_area.setText(current_text)
        
        for label in self.settings_tab.findChildren(ModernLabel):
            if label.text() in ["Language", "Theme", "Mode", "Язык", "Тема", "Режим", "Sprache", "Thema", "Modus"]:
                if label.text() in ["Language", "Язык", "Sprache"]:
                    label.setText(self.tr("Language"))
                elif label.text() in ["Theme", "Тема", "Thema"]:
                    label.setText(self.tr("Theme"))
                elif label.text() in ["Mode", "Режим", "Modus"]:
                    label.setText(self.tr("Mode"))
        
        for btn in self.findChildren(ModernButton):
            if btn.text() in ["Clear History", "Очистить историю", "Geschichte löschen"]:
                btn.setText(self.tr("Clear History"))


if __name__ == '__main__':
    loader.main()
    
    app = QApplication(sys.argv)
    
    app.setFont(QFont("Segoe UI", 10))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
