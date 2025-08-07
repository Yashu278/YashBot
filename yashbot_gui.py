import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
    QLabel, QComboBox, QMessageBox, QFrame, QSplitter, QScrollArea, QGridLayout,
    QProgressBar, QSlider, QCheckBox, QGroupBox, QTabWidget, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QFont, QColor, QTextCursor, QPalette, QPixmap, QIcon, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty
from dotenv import load_dotenv
from core.online_model import online_chat
from core.offline_model import offline_chat
import datetime

# Load environment variables
load_dotenv()

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(-2, -2, 2, 2))
        self._animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(2, 2, -2, -2))
        self._animation.start()
        super().leaveEvent(event)

class ChatBubble(QFrame):
    def __init__(self, text, is_user=True, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(0)
        self.setMaximumWidth(400)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Message label
        msg_label = QLabel(text)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet(f"""
            QLabel {{
                background-color: {'#6272a4' if is_user else '#44475a'};
                color: #f8f8f2;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                line-height: 1.4;
            }}
        """)
        
        # Time label
        time_label = QLabel(datetime.datetime.now().strftime("%H:%M"))
        time_label.setStyleSheet("color: #6272a4; font-size: 11px; margin-top: 5px;")
        time_label.setAlignment(Qt.AlignRight)
        
        layout.addWidget(msg_label)
        layout.addWidget(time_label)
        
        # Align based on user/bot
        if is_user:
            layout.setAlignment(Qt.AlignRight)
        else:
            layout.setAlignment(Qt.AlignLeft)

class YashBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YashBot - AI Assistant")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        self.chat_history = []
        self.chat_model = None
        self.init_ui()
        self.select_mode()
        self.setup_animations()

    def init_ui(self):
        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # Left panel (sidebar)
        self.create_sidebar()
        main_layout.addWidget(self.sidebar, 1)
        
        # Right panel (chat area)
        self.create_chat_area()
        main_layout.addWidget(self.chat_widget, 3)
        
        # Apply dark theme
        self.apply_dark_theme()

    def create_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setMaximumWidth(250)
        self.sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d3748, stop:1 #1a202c);
                border-right: 1px solid #4a5568;
            }
        """)
        
        sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(sidebar_layout)
        
        # Logo/Title
        title = QLabel("🤖 YashBot")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #8be9fd; margin: 20px;")
        title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title)
        
        # Status indicator
        self.status_label = QLabel("● Offline")
        self.status_label.setStyleSheet("color: #ff5555; font-size: 12px; margin: 10px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(self.status_label)
        
        # Mode selection
        mode_group = QGroupBox("AI Mode")
        mode_group.setStyleSheet("""
            QGroupBox {
                color: #f8f8f2;
                font-weight: bold;
                border: 1px solid #4a5568;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        mode_layout = QVBoxLayout()
        mode_group.setLayout(mode_layout)
        
        self.online_btn = AnimatedButton("🌐 Online Mode")
        self.offline_btn = AnimatedButton("💻 Offline Mode")
        
        for btn in [self.online_btn, self.offline_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4a5568, stop:1 #2d3748);
                    color: #f8f8f2;
                    border: 1px solid #4a5568;
                    border-radius: 8px;
                    padding: 12px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #5a6a8a, stop:1 #3d4a6a);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3d4a6a, stop:1 #2d3748);
                }
            """)
            mode_layout.addWidget(btn)
        
        self.online_btn.clicked.connect(lambda: self.set_mode("online"))
        self.offline_btn.clicked.connect(lambda: self.set_mode("offline"))
        sidebar_layout.addWidget(mode_group)
        
        # Settings
        settings_group = QGroupBox("Settings")
        settings_group.setStyleSheet("""
            QGroupBox {
                color: #f8f8f2;
                font-weight: bold;
                border: 1px solid #4a5568;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        settings_layout = QVBoxLayout()
        settings_group.setLayout(settings_layout)
        
        # Temperature slider
        temp_label = QLabel("Temperature: 0.7")
        temp_label.setStyleSheet("color: #f8f8f2; font-size: 12px;")
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setRange(0, 100)
        self.temp_slider.setValue(70)
        self.temp_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #4a5568;
                height: 8px;
                background: #2d3748;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #8be9fd;
                border: 1px solid #8be9fd;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)
        self.temp_slider.valueChanged.connect(
            lambda v: temp_label.setText(f"Temperature: {v/100:.1f}")
        )
        
        settings_layout.addWidget(temp_label)
        settings_layout.addWidget(self.temp_slider)
        sidebar_layout.addWidget(settings_group)
        
        # Spacer
        sidebar_layout.addStretch()
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("color: #6272a4; font-size: 11px; margin: 10px;")
        version_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(version_label)

    def create_chat_area(self):
        self.chat_widget = QWidget()
        chat_layout = QVBoxLayout()
        self.chat_widget.setLayout(chat_layout)
        
        # Chat header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d3748, stop:1 #1a202c);
                border-bottom: 1px solid #4a5568;
                padding: 10px;
            }
        """)
        header_layout = QHBoxLayout()
        header.setLayout(header_layout)
        
        self.chat_title = QLabel("💬 Chat with YashBot")
        self.chat_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.chat_title.setStyleSheet("color: #8be9fd;")
        header_layout.addWidget(self.chat_title)
        
        # Clear chat button
        clear_btn = AnimatedButton("🗑️ Clear")
        clear_btn.setStyleSheet("""
            QPushButton {
                background: #ff5555;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #ff6b6b;
            }
        """)
        clear_btn.clicked.connect(self.clear_chat)
        header_layout.addWidget(clear_btn)
        
        chat_layout.addWidget(header)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 12))
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #1a202c;
                color: #f8f8f2;
                border: none;
                padding: 20px;
                line-height: 1.6;
            }
        """)
        chat_layout.addWidget(self.chat_display, 1)
        
        # Input area
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d3748, stop:1 #1a202c);
                border-top: 1px solid #4a5568;
                padding: 15px;
            }
        """)
        input_layout = QHBoxLayout()
        input_frame.setLayout(input_layout)
        
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message here...")
        self.input_box.setStyleSheet("""
            QLineEdit {
                background-color: #2d3748;
                color: #f8f8f2;
                border: 2px solid #4a5568;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #8be9fd;
            }
        """)
        self.input_box.returnPressed.connect(self.send_message)
        
        self.send_btn = AnimatedButton("🚀 Send")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #50fa7b, stop:1 #3d8a5a);
                color: #1a202c;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6aff8d, stop:1 #4daa6a);
            }
        """)
        self.send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_box, 1)
        input_layout.addWidget(self.send_btn)
        chat_layout.addWidget(input_frame)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1a202c;
                color: #f8f8f2;
            }
        """)

    def setup_animations(self):
        # Fade in animation
        self.setWindowOpacity(0.0)
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

    def set_mode(self, mode):
        if mode == "online":
            self.chat_model = online_chat
            self.status_label.setText("● Online")
            self.status_label.setStyleSheet("color: #50fa7b; font-size: 12px; margin: 10px;")
            self.append_system_message("✅ Switched to Online mode (OpenRouter API)")
        else:
            self.chat_model = offline_chat
            self.status_label.setText("● Offline")
            self.status_label.setStyleSheet("color: #ffb86c; font-size: 12px; margin: 10px;")
            self.append_system_message("✅ Switched to Offline mode (local GPT4All)")

    def select_mode(self):
        # Auto-select online mode by default
        self.set_mode("online")

    def append_system_message(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M")
        self.chat_display.append(f'<div style="text-align: center; color: #6272a4; font-size: 12px; margin: 10px 0;">{message} • {timestamp}</div>')
        self.chat_display.moveCursor(QTextCursor.End)

    def append_user_message(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M")
        self.chat_display.append(f'''
            <div style="text-align: right; margin: 10px 0;">
                <div style="display: inline-block; background: #6272a4; color: #f8f8f2; padding: 10px 15px; border-radius: 15px; max-width: 70%;">
                    {message}
                </div>
                <div style="color: #6272a4; font-size: 11px; margin-top: 5px;">{timestamp}</div>
            </div>
        ''')
        self.chat_display.moveCursor(QTextCursor.End)

    def append_bot_message(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M")
        self.chat_display.append(f'''
            <div style="text-align: left; margin: 10px 0;">
                <div style="display: inline-block; background: #44475a; color: #f8f8f2; padding: 10px 15px; border-radius: 15px; max-width: 70%;">
                    {message}
                </div>
                <div style="color: #6272a4; font-size: 11px; margin-top: 5px;">{timestamp}</div>
            </div>
        ''')
        self.chat_display.moveCursor(QTextCursor.End)

    def send_message(self):
        user_input = self.input_box.text().strip()
        if not user_input:
            return
        
        self.append_user_message(user_input)
        self.input_box.clear()
        QApplication.processEvents()
        
        # Show typing indicator
        self.chat_display.append('<div style="text-align: left; margin: 10px 0;"><div style="display: inline-block; background: #44475a; color: #f8f8f2; padding: 10px 15px; border-radius: 15px;">🤖 Thinking...</div></div>')
        self.chat_display.moveCursor(QTextCursor.End)
        QApplication.processEvents()
        
        # Get bot response
        try:
            if self.chat_model:
                response = self.chat_model(user_input)
            else:
                response = "⚠ Please select a mode first!"
        except Exception as e:
            response = f"⚠ Error: {e}"
        
        # Remove typing indicator and add response
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.deletePreviousChar()  # Remove the extra newline
        
        self.append_bot_message(response)

    def clear_chat(self):
        self.chat_display.clear()
        self.append_system_message("Chat cleared")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    window = YashBotGUI()
    window.show()
    sys.exit(app.exec_())
