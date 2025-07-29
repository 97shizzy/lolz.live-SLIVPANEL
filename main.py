#полу гпт полу мой первый нормальный код все настройки елси что хранятся в реестре по пути HKEY_CURRENT_USER\Software\LolzPanel\SlivPanel, на ост ОС гуглите у pyside 
#всегда все одинаково, вроде норм получилось

import subprocess
import os
import sys
import requests
import json
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QMessageBox, QSpacerItem, QSizePolicy, QScrollArea, QCheckBox, 
    QGridLayout, QFileDialog, QHBoxLayout, QColorDialog, QComboBox, QMenu,
    QDialog, QTextEdit
)
from PySide6.QtGui import QFont, QColor, QAction
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QEvent, QRect, QSettings
from PySide6.QtWidgets import QGraphicsDropShadowEffect

PREFIXES = [
    {"prefix_id": 91, "prefix_title": "Видео"},
    {"prefix_id": 182, "prefix_title": "OnlyFans"},
    {"prefix_id": 290, "prefix_title": "Пак"},
    {"prefix_id": 319, "prefix_title": "Patreon"},
    {"prefix_id": 598, "prefix_title": "Косплей"},
    {"prefix_id": 603, "prefix_title": "Приватки TG"},
    {"prefix_id": 604, "prefix_title": "Boosty"},
    {"prefix_id": 605, "prefix_title": "Fansly"},
    {"prefix_id": 606, "prefix_title": "Дамп"},
]

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Настройки")
        self.setFixedSize(800, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: #1b0000;
                color: #f0f0f0;
            }
            QLabel {
                color: #ff6666;
            }
            QLineEdit, QTextEdit {
                background-color: #330000;
                border: 2px solid #cc2222;
                border-radius: 10px;
                padding: 8px;
                color: white;
                selection-background-color: #ff5555;
            }
            QPushButton {
                background-color: #660000;
                border: 2px solid #ff4444;
                border-radius: 10px;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #880000;
            }
            QPushButton:pressed {
                background-color: #440000;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        
        token_layout = QVBoxLayout()
        token_layout.setSpacing(5)
        
        token_label = QLabel("Bearer Token:")
        token_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        self.token_edit = QLineEdit()
        self.token_edit.setFont(QFont("Segoe UI", 11))
        self.token_edit.setPlaceholderText("Введите ваш Bearer Token")
        token_layout.addWidget(token_label)
        token_layout.addWidget(self.token_edit)

        template_layout = QVBoxLayout()
        template_layout.setSpacing(5)
        
        template_label = QLabel("Шаблон поста BBCODE, пример можно найти в patern.txt: ")
        template_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        self.template_edit = QTextEdit()
        self.template_edit.setFont(QFont("Segoe UI", 11))
        self.template_edit.setPlaceholderText(
            "Доступные переменные:\n"
            "{color_r}, {color_g}, {color_b} - RGB цвет\n"
            "{post_header} - Текст заголовка\n"
            "{mega_link} - Ссылка на Mega\n"
            "{likes} - Лимит лайков\n"
            "{button_url} - URL кнопки\n"
            "{button_text} - Текст кнопки\n"
            "ЭТО ВАЖНО БЕЗ ИХ ИСПОЛЬЗОВАНИЯ ТЕМА БУДЕТ СОЗДАНА КРИВО\n"
            "КАЖДАЯ ОТВЕЧАЕТ ЗА СВОЮ НАСТРОЙКУ\n"
            
        )
        self.template_edit.setFixedHeight(300)
        
        template_layout.addWidget(template_label)
        template_layout.addWidget(self.template_edit)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(5)
        
        button_text_label = QLabel("Текст кнопки:")
        button_text_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        self.button_text_edit = QLineEdit()
        self.button_text_edit.setFont(QFont("Segoe UI", 11))
        
        button_url_label = QLabel("URL кнопки:")
        button_url_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        self.button_url_edit = QLineEdit()
        self.button_url_edit.setFont(QFont("Segoe UI", 11))
        
        button_layout.addWidget(button_text_label)
        button_layout.addWidget(self.button_text_edit)
        button_layout.addWidget(button_url_label)
        button_layout.addWidget(self.button_url_edit)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.save_btn.clicked.connect(self.save_settings)
        
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setFont(QFont("Segoe UI", 12))
        self.cancel_btn.clicked.connect(self.close)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.save_btn)

        layout.addLayout(token_layout)
        layout.addLayout(template_layout)
        layout.addLayout(button_layout)
        layout.addStretch()
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        self.load_settings()

    def load_settings(self):
        settings = QSettings("LolzPanel", "SlivPanel")
        self.token_edit.setText(settings.value("bearer_token", ""))
        self.template_edit.setPlainText(settings.value("post_template", 
            "[CENTER][COLOR=rgb({color_r},{color_g},{color_b})][SIZE=5]{post_header}[/SIZE][/COLOR][/CENTER]\n"
            "[likes={likes};align=center][URL=\"{mega_link}\"]ССЫЛКА МЕГА[/URL][/likes]\n"
            "[CENTER][Button={button_url}]{button_text}[/button][/CENTER]"))
        self.button_text_edit.setText(settings.value("button_text", "ЗАХОДИТЕ И ГОЛОСУЙТЕ ЗА ПРЕДЛОЖЕНИЕ ДОБАВЛЕНИЯ ЗАГРУЗКИ АУДИО"))
        self.button_url_edit.setText(settings.value("button_url", "https://lolz.live/threads/8864532/"))
    def save_settings(self):
        settings = QSettings("LolzPanel", "SlivPanel")
        settings.setValue("bearer_token", self.token_edit.text())
        settings.setValue("post_template", self.template_edit.toPlainText())
        settings.setValue("button_text", self.button_text_edit.text())
        settings.setValue("button_url", self.button_url_edit.text())
        
        self.parent.load_settings()
        QMessageBox.information(self, "Сохранено", "Настройки успешно сохранены!")
        self.close()

class LolzPostGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sliv 18+ PANEL|Created by: @rasez TG: @N0S3NSE for Lolz.live")
        self.setMinimumSize(920, 935)
        self.setStyleSheet("""
            QWidget {
                background-color: #1b0000;
                color: #f0f0f0;
            }
            QLabel {
                color: #ff6666;
            }
            QLineEdit {
                background-color: #330000;
                border: 2px solid #cc2222;
                border-radius: 14px;
                padding: 10px 12px;
                color: #fff;
                selection-background-color: #ff5555;
                font-weight: 600;
            }
            QLineEdit:focus {
                border-color: #ff6666;
                background-color: #440000;
            }
            QPushButton {
                background-color: #660000;
                border: 2px solid #ff4444;
                border-radius: 10px;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #880000;
            }
            QPushButton:pressed {
                background-color: #440000;
            }
        """)
        
        self.color_r = 242
        self.color_g = 46
        self.color_b = 160
        self.setup_ui()
        self.fade_in()
        self.load_settings()

    def load_settings(self):
        settings = QSettings("LolzPanel", "SlivPanel")
        self.bearer_token = settings.value("bearer_token", "Bearer YOUR_TOKEN_HERE")
        self.post_template = settings.value("post_template", 
            "[CENTER][COLOR=rgb({color_r},{color_g},{color_b})][SIZE=5]{post_header}[/SIZE][/COLOR][/CENTER]\n"
            "[likes={likes};align=center][URL=\"{mega_link}\"]ССЫЛКА МЕГА[/URL][/likes]\n"
            "[CENTER][Button={button_url}]{button_text}[/button][/CENTER]")
        self.button_text = settings.value("button_text", "ЗАХОДИТЕ И ГОЛОСУЙТЕ ЗА ПРЕДЛОЖЕНИЕ ДОБАВЛЕНИЯ ЗАГРУЗКИ АУДИО")
        self.button_url = settings.value("button_url", "https://lolz.live/threads/8864532/")
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
    
        menu_btn = QPushButton("МЕНЮ<3")
        menu_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        menu_btn.setFixedWidth(120)
        menu_btn.clicked.connect(self.show_menu)
    
        top_layout = QHBoxLayout()
        top_layout.addWidget(menu_btn)
        top_layout.addStretch()
    
        title_label = QLabel("Заголовок темы")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
    
        self.title_edit = QLineEdit()
        self.title_edit.setFont(QFont("Segoe UI", 14))
    
        post_header_label = QLabel("Текст в теме")
        post_header_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
    
        self.post_header_edit = QLineEdit()
        self.post_header_edit.setFont(QFont("Segoe UI", 14))
    
        self.color_btn = QPushButton("Выбрать цвет текста")
        self.color_btn.setFont(QFont("Segoe UI", 12))
        self.color_btn.clicked.connect(self.choose_color)
        self.update_color_button()
    
        mega_label = QLabel("Ссылка на Mega.nz")
        mega_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
    
        self.mega_edit = QLineEdit()
        self.mega_edit.setFont(QFont("Segoe UI", 14))
    
        self.upload_btn = QPushButton("Загрузить папку на Mega")
        self.upload_btn.setFont(QFont("Segoe UI", 12))
        self.upload_btn.clicked.connect(self.upload_to_mega)
    
        mega_layout = QHBoxLayout()
        mega_layout.addWidget(self.mega_edit, 1)
        mega_layout.addWidget(self.upload_btn)
    
        likes_label = QLabel("Лимит лайков")
        likes_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
    
        self.likes_edit = QLineEdit()
        self.likes_edit.setFont(QFont("Segoe UI", 14))
        self.likes_edit.setPlaceholderText("11923812981273198231730938")
    
    # Prefixes
        prefix_label = QLabel("Выберите префиксы в теме")
        prefix_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
    
        self.prefix_checkboxes = []
        prefix_grid = QGridLayout()
        prefix_grid.setHorizontalSpacing(20)
        prefix_grid.setVerticalSpacing(10)
    
        for i, prefix in enumerate(PREFIXES):
            checkbox = QCheckBox(prefix["prefix_title"])
            checkbox.setFont(QFont("Segoe UI", 12, QFont.Bold))
            checkbox.setStyleSheet("""
            QCheckBox {
                color: #ff6666;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #cc2222;
                background-color: #330000;
                border-radius: 5px;
            }
            QCheckBox::indicator:checked {
                background-color: #ff4444;
                border: 2px solid #ff8888;
                border-radius: 5px;
            }
        """)
            self.prefix_checkboxes.append((checkbox, prefix["prefix_id"], prefix["prefix_title"]))
            prefix_grid.addWidget(checkbox, i // 3, i % 3)
    
        prefix_widget = QWidget()
        prefix_widget.setLayout(prefix_grid)
    
        prefix_scroll = QScrollArea()
        prefix_scroll.setWidgetResizable(True)
        prefix_scroll.setWidget(prefix_widget)
        prefix_scroll.setFixedHeight(150)
    
    
        self.schedule_checkbox = QCheckBox("Отложить публикацию темы")
        self.schedule_checkbox.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.schedule_checkbox.setStyleSheet("""
        QCheckBox {
            color: #ff6666;
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
        }
        QCheckBox::indicator:unchecked {
            border: 2px solid white;
            background-color: #330000;
            border-radius: 5px;
        }
        QCheckBox::indicator:checked {
            background-color: #ff4444;
            border: 2px solid yellow;
            border-radius: 5px;
        }
    """)
        schedule_layout = QHBoxLayout()
        schedule_layout.setSpacing(10)
        
        self.date_edit = QLineEdit()
        self.date_edit.setFont(QFont("Segoe UI", 12))
        self.date_edit.setPlaceholderText("ДД-ММ-ГГГГ")
        self.date_edit.setFixedWidth(150)
        
        self.time_edit = QLineEdit()
        self.time_edit.setFont(QFont("Segoe UI", 12))
        self.time_edit.setPlaceholderText("ЧЧ:ММ")
        self.time_edit.setFixedWidth(100)

        schedule_layout.addWidget(QLabel("Дата:"))
        schedule_layout.addWidget(self.date_edit)
        schedule_layout.addWidget(QLabel("Время:"))
        schedule_layout.addWidget(self.time_edit)
        schedule_layout.addStretch()
        
        self.schedule_widget = QWidget()
        self.schedule_widget.setLayout(schedule_layout)
        self.send_btn = QPushButton("Запостить тему")
        self.send_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.send_btn.setFixedHeight(50)
        self.send_btn.clicked.connect(self.send_request)
    
        layout.addLayout(top_layout)
        layout.addWidget(title_label)
        layout.addWidget(self.title_edit)
        layout.addWidget(post_header_label)
        layout.addWidget(self.post_header_edit)
        layout.addWidget(self.color_btn)
        layout.addWidget(mega_label)
        layout.addLayout(mega_layout)
        layout.addWidget(likes_label)
        layout.addWidget(self.likes_edit)
        layout.addWidget(prefix_label)
        layout.addWidget(prefix_scroll)
        layout.addWidget(self.schedule_checkbox)
        layout.addWidget(self.schedule_widget)
        layout.addWidget(self.send_btn)
    
        self.setLayout(layout)
    
    def toggle_schedule_fields(self, state):
        self.schedule_widget.setEnabled(state == Qt.Checked)
        self.date_edit.setEnabled(state == Qt.Checked)
        self.time_edit.setEnabled(state == Qt.Checked)
    
    def validate_schedule(self):
        if not self.schedule_checkbox.isChecked():
            return True, None, None
        
        date_str = self.date_edit.text().strip()
        time_str = self.time_edit.text().strip()
        
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            datetime.strptime(time_str, "%H:%M")
            return True, date_str, time_str
        except ValueError:
            QMessageBox.warning(
                self, 
                "Ошибка формата", 
                "Проверьте формат даты и времени!\n"
                "Дата: ДД-ММ-ГГГГ (например, 30-07-2025)\n"
                "Время: ЧЧ:ММ (например, 14:30)"
            )
            return False, None, None

    def update_color_button(self):
        self.color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgb({self.color_r}, {self.color_g}, {self.color_b});
                color: white;
                border: 1px solid #ff4444;
                border-radius: 8px;
                padding: 5px;
            }}
        """)

    def show_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #330000;
                border: 1px solid #ff4444;
                color: white;
            }
            QMenu::item:selected {
                background-color: #660000;
            }
        """)
        
        settings_action = QAction("Настройки", self)
        settings_action.triggered.connect(self.open_settings)
        menu.addAction(settings_action)
        
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)
        
        menu.exec(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def show_about(self):
        QMessageBox.about(self, "О программе", 
                        "Sliv Panel Lolzik PRO\n\n"
                        "Версия: 2.0\n"
                        "Автор: rasez\n\n"
                        "Программа для автоматического создания тем на Lolz.live сливЫ")

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_r = color.red()
            self.color_g = color.green()
            self.color_b = color.blue()
            self.update_color_button()

    def upload_to_mega(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для загрузки")
        if not folder:
            return
        folder = os.path.normpath(folder)
        folder_name = os.path.basename(folder)
        remote_folder = f"/{folder_name}"
        try:
            subprocess.run(["mega-mkdir", remote_folder], check=True, shell=True)

            for root, dirs, files in os.walk(folder):
                relative_path = os.path.relpath(root, folder)
                remote_path = os.path.join(remote_folder, relative_path).replace("\\", "/")

                if relative_path != ".":
                    subprocess.run(["mega-mkdir", remote_path], check=True, shell=True)

                for file in files:
                    local_file = os.path.normpath(os.path.join(root, file))
                    subprocess.run(["mega-put", local_file, remote_path], check=True, shell=True)

            result = subprocess.run(
                ["mega-export", "-a", remote_folder],
                capture_output=True,
                text=True,
                shell=True
            )
        
            if result.returncode == 0:
                link = result.stdout.strip()

                if ":" in link:
                    link = link.split(":")[-1].strip()

                if link.startswith("//"):
                    link = "https:" + link

                link = link.replace("\n", "").replace("\r", "")

                self.mega_edit.setText(link)
                QMessageBox.information(self, "Успех", f"Папка загружена!\nСсылка: {link}")
            else:
                QMessageBox.warning(self, "Ошибка", f"Ошибка получения ссылки:\n{result.stderr}")

        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки:\n{e.stderr}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Неизвестная ошибка:\n{str(e)}")

    def fade_in(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(600)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()
    def send_request(self):
        title = self.title_edit.text().strip()
        post_header = self.post_header_edit.text().strip()
        mega_link = self.mega_edit.text().strip()
        likes = self.likes_edit.text().strip()

        if not title or not post_header or not mega_link or not likes:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля!")
            return

        if not likes.isdigit():
            QMessageBox.warning(self, "Ошибка", "Поле 'Лимит' должно быть числом!")
            return

        selected_prefixes = [(pid, title) for cb, pid, title in self.prefix_checkboxes if cb.isChecked()]
        if not selected_prefixes:
            QMessageBox.warning(self, "Ошибка", "Выберите хотя бы один префикс!")
            return
            
        
        schedule_valid, schedule_date, schedule_time = self.validate_schedule()
        if not schedule_valid:
            return
            
        prefix_part = "".join([f"&prefix_id[]={p[0]}" for p in selected_prefixes])
        encoded_title = requests.utils.quote(title)

        url = (
            f"https://api.lolz.live/threads?"
            f"forum_id=775&title={encoded_title}"
            f"{prefix_part}"
            "&tags=%D0%A1%D0%BB%D0%B8%D0%B2%D1%8B,18%2B,%D0%90%D0%BB%D1%8C%D1%82%D1%83%D1%88%D0%BA%D0%B8,%D0%A8%D0%BB%D0%BE%D1%88%D0%BA%D0%B8"
            "&allow_ask_hidden_content=true"
        )

        post_body = self.post_template.format(
            color_r=self.color_r,
            color_g=self.color_g,
            color_b=self.color_b,
            post_header=post_header,
            mega_link=mega_link,
            likes=likes,
            button_url=self.button_url,
            button_text=self.button_text
        )

        payload = {
            "post_body": post_body,
            "enable_schedule": self.schedule_checkbox.isChecked()
        }
        
        if self.schedule_checkbox.isChecked():
            payload["schedule_date"] = schedule_date
            payload["schedule_time"] = schedule_time

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.bearer_token
        }
    
        if not self.bearer_token.startswith("Bearer "):
            headers["authorization"] = "Bearer " + self.bearer_token.strip()
    
        try:
            response = requests.post(url, json=payload, headers=headers)
    
            if response.status_code == 401:
                QMessageBox.critical(
                    self, 
                    "Ошибка авторизации", 
                    "Неверный токен! Обновите его в настройках.\n"
                    f"Ответ сервера: {response.text}"
                )
                self.open_settings()
                return
        
            elif response.status_code in [200, 201]:
                if self.schedule_checkbox.isChecked():
                    QMessageBox.information(
                        self, 
                        "Успех", 
                        f"Тема успешно запланирована на {schedule_date} {schedule_time}!"
                    )
                else:
                    QMessageBox.information(self, "Успех", "Тема успешно создана!")
                
                self.save_log(title, mega_link, post_body, likes, selected_prefixes)
        
            else:
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    f"Ошибка при создании темы: {response.status_code}\n{response.text}"
                )

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self,
                "Ошибка соединения",
                f"Не удалось отправить запрос:\n{str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Неизвестная ошибка",
                f"Произошла ошибка:\n{str(e)}"
            )

    def save_log(self, title, mega, header, limit, prefixes):
        data = {
            "title": title,
            "mega": mega,
            "post_header": header,
            "limit": limit,
            "prefixes": [p[1] for p in prefixes],
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "color": f"rgb({self.color_r},{self.color_g},{self.color_b})"
        }
    

        if self.schedule_checkbox.isChecked():
            data["scheduled_date"] = self.date_edit.text()
            data["scheduled_time"] = self.time_edit.text()
    
        try:
            with open("log.json", "a", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False, indent=4))
                f.write("\n\n")
        except Exception as e:
            print("Ошибка сохранения лога:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LolzPostGUI()
    window.show()
    sys.exit(app.exec())
