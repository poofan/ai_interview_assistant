"""
Update Dialog - [АЗ + ДОБРО]
GUI диалог для уведомлений об обновлениях
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from loguru import logger
from typing import Dict, Optional
import webbrowser


class UpdateDialog(QDialog):
    """
    Диалог обновления приложения
    Архетипы:
    - АЗ: управление доступом к обновлениям
    - ДОБРО: информирование пользователя
    """
    
    def __init__(self, update_info: Dict, parent=None):
        """
        Инициализация диалога обновления
        
        Args:
            update_info: Информация об обновлении
            parent: Родительский виджет
        """
        super().__init__(parent)
        self.update_info = update_info
        self.user_choice = None  # "download", "later", "skip"
        
        self._init_ui()
    
    def _init_ui(self):
        """
        Инициализация интерфейса
        """
        self.setWindowTitle("🆕 Доступно обновление Hintsage")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        # Основной layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Заголовок
        title_label = QLabel(f"📦 Новая версия {self.update_info.get('version', 'N/A')} доступна!")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Информация о версии
        version_info = QLabel(
            f"Текущая версия: {self.update_info.get('current_version', 'N/A')}\n"
            f"Новая версия: {self.update_info.get('version', 'N/A')}\n"
            f"Дата выпуска: {self.update_info.get('release_date', 'N/A')}"
        )
        version_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_info)
        
        # Критическое обновление
        if self.update_info.get('critical', False):
            critical_label = QLabel("⚠️ КРИТИЧЕСКОЕ ОБНОВЛЕНИЕ ⚠️")
            critical_font = QFont()
            critical_font.setPointSize(12)
            critical_font.setBold(True)
            critical_label.setFont(critical_font)
            critical_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            critical_label.setStyleSheet("color: red;")
            layout.addWidget(critical_label)
        
        # Changelog
        changelog_label = QLabel("📝 Что нового:")
        changelog_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(changelog_label)
        
        changelog_text = QTextEdit()
        changelog_text.setReadOnly(True)
        changelog_text.setMaximumHeight(200)
        
        # Форматируем changelog
        changelog = self.update_info.get('changelog', [])
        if isinstance(changelog, list):
            changelog_text.setPlainText("\n".join([f"• {item}" for item in changelog]))
        else:
            changelog_text.setPlainText(str(changelog))
        
        layout.addWidget(changelog_text)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        # Кнопка "Скачать"
        download_btn = QPushButton("⬇️ Скачать обновление")
        download_btn.setStyleSheet(
            "QPushButton {"
            "   background-color: #4CAF50;"
            "   color: white;"
            "   padding: 10px;"
            "   font-size: 12pt;"
            "   border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #45a049;"
            "}"
        )
        download_btn.clicked.connect(self._on_download)
        button_layout.addWidget(download_btn)
        
        # Кнопка "Позже"
        if not self.update_info.get('critical', False):
            later_btn = QPushButton("⏰ Напомнить позже")
            later_btn.clicked.connect(self._on_later)
            button_layout.addWidget(later_btn)
        
        # Кнопка "Пропустить"
        if not self.update_info.get('critical', False):
            skip_btn = QPushButton("❌ Пропустить эту версию")
            skip_btn.clicked.connect(self._on_skip)
            button_layout.addWidget(skip_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _on_download(self):
        """
        Обработчик кнопки "Скачать"
        """
        download_url = self.update_info.get('download_url', '')
        
        if download_url:
            logger.info(f"🌐 Открываем страницу загрузки: {download_url}")
            try:
                webbrowser.open(download_url)
                self.user_choice = "download"
                self.accept()
            except Exception as e:
                logger.error(f"❌ Ошибка открытия браузера: {e}")
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    f"Не удалось открыть браузер.\nСкопируйте ссылку вручную:\n{download_url}"
                )
        else:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Ссылка на загрузку недоступна.\nОбратитесь в поддержку."
            )
    
    def _on_later(self):
        """
        Обработчик кнопки "Позже"
        """
        logger.info("⏰ Пользователь отложил обновление")
        self.user_choice = "later"
        self.accept()
    
    def _on_skip(self):
        """
        Обработчик кнопки "Пропустить"
        """
        logger.info("❌ Пользователь пропустил обновление")
        self.user_choice = "skip"
        self.accept()
    
    def get_user_choice(self) -> Optional[str]:
        """
        Получить выбор пользователя
        
        Returns:
            "download", "later", "skip" или None
        """
        return self.user_choice


def show_update_dialog(update_info: Dict, parent=None) -> Optional[str]:
    """
    Показать диалог обновления
    
    Args:
        update_info: Информация об обновлении
        parent: Родительский виджет
    
    Returns:
        Выбор пользователя: "download", "later", "skip" или None
    """
    dialog = UpdateDialog(update_info, parent)
    dialog.exec()
    return dialog.get_user_choice()

