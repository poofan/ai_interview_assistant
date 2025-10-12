"""
Error Handler - [ШТОР + ЧЕЛО]
Обработка ошибок и пользовательские уведомления
"""

import re
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import QMessageBox, QWidget
from loguru import logger


class ErrorHandler:
    """
    Обработчик ошибок с пользовательским интерфейсом
    Архетипы:
    - ШТОР: защита от ошибок
    - ЧЕЛО: взаимодействие с пользователем
    """
    
    def __init__(self, parent_widget: Optional[QWidget] = None):
        """
        Инициализация обработчика ошибок
        
        Args:
            parent_widget: Родительский виджет для диалогов
        """
        self.parent_widget = parent_widget
        
        # Паттерны ошибок OpenAI
        self.error_patterns = {
            "unsupported_country": r"unsupported_country_region_territory",
            "invalid_api_key": r"invalid_api_key|authentication_failed",
            "rate_limit": r"rate_limit_exceeded",
            "quota_exceeded": r"quota_exceeded",
            "model_not_found": r"model_not_found",
            "network_error": r"network|connection|timeout",
            "no_valid_keys": r"no_valid_keys",
        }
    
    def handle_api_error(self, error_message: str, error_code: str = "", error_details: dict = None) -> None:
        """
        Обработать ошибку API и показать пользователю
        
        Args:
            error_message: Сообщение об ошибке
            error_code: Код ошибки (если есть)
            error_details: Детальная информация об ошибке
        """
        logger.error(f"API Error: {error_code} - {error_message}")
        
        # Определяем тип ошибки
        error_type = self._detect_error_type(error_message, error_code)
        
        # Показываем соответствующее уведомление
        self._show_error_dialog(error_type, error_message, error_code, error_details)
    
    def _detect_error_type(self, message: str, code: str) -> str:
        """
        Определить тип ошибки по сообщению и коду
        
        Args:
            message: Сообщение об ошибке
            code: Код ошибки
            
        Returns:
            Тип ошибки
        """
        combined_text = f"{message} {code}".lower()
        
        for error_type, pattern in self.error_patterns.items():
            if re.search(pattern, combined_text, re.IGNORECASE):
                return error_type
        
        return "generic"
    
    def _show_error_dialog(self, error_type: str, message: str, code: str, error_details: dict = None) -> None:
        """
        Показать диалог с ошибкой пользователю
        
        Args:
            error_type: Тип ошибки
            message: Сообщение об ошибке
            code: Код ошибки
            error_details: Детальная информация об ошибке
        """
        dialog = QMessageBox(self.parent_widget)
        dialog.setWindowTitle("⚠️ Ошибка Hintsage")
        
        # Если есть детальная информация, используем её
        if error_details and "suggestion" in error_details:
            suggestion = error_details["suggestion"]
        else:
            suggestion = "Попробуйте перезапустить приложение"
        
        if error_type == "unsupported_country":
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.setText("🌐 OpenAI недоступен в вашем регионе")
            dialog.setInformativeText(
                f"Для использования Hintsage необходимо подключение через VPN.\n\n"
                f"Решение:\n"
                f"1. Включите VPN (рекомендуем серверы США или Европы)\n"
                f"2. Убедитесь, что VPN работает корректно\n"
                f"3. Перезапустите приложение\n"
                f"4. Попробуйте снова\n\n"
                f"💡 Совет: {suggestion}"
            )
            dialog.setDetailedText(f"Техническая информация:\n{code}: {message}")
            
        elif error_type == "invalid_api_key":
            dialog.setIcon(QMessageBox.Icon.Critical)
            dialog.setText("🔑 Проблема с API ключом")
            dialog.setInformativeText(
                "Обнаружена проблема с API ключом OpenAI.\n\n"
                "Это может быть связано с:\n"
                "• Истекшим сроком действия ключа\n"
                "• Превышением лимитов\n"
                "• Техническими проблемами сервера"
            )
            dialog.setDetailedText(f"Техническая информация:\n{code}: {message}")
            
        elif error_type == "rate_limit":
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.setText("⏱️ Превышен лимит запросов")
            dialog.setInformativeText(
                "Слишком много запросов к OpenAI API.\n\n"
                "Пожалуйста, подождите несколько минут и попробуйте снова."
            )
            dialog.setDetailedText(f"Техническая информация:\n{code}: {message}")
            
        elif error_type == "quota_exceeded":
            dialog.setIcon(QMessageBox.Icon.Critical)
            dialog.setText("💳 Превышена квота API")
            dialog.setInformativeText(
                "Превышен лимит использования OpenAI API.\n\n"
                "Необходимо пополнить баланс или дождаться обновления квоты."
            )
            dialog.setDetailedText(f"Техническая информация:\n{code}: {message}")
            
        elif error_type == "model_not_found":
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.setText("🤖 Модель недоступна")
            dialog.setInformativeText(
                "Выбранная модель OpenAI недоступна.\n\n"
                "Попробуйте изменить модель в настройках."
            )
            dialog.setDetailedText(f"Техническая информация:\n{code}: {message}")
            
        elif error_type == "network_error":
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.setText("🌐 Проблема с сетью")
            dialog.setInformativeText(
                "Не удается подключиться к серверу OpenAI.\n\n"
                "Проверьте:\n"
                "• Подключение к интернету\n"
                "• Настройки VPN\n"
                "• Брандмауэр"
            )
            dialog.setDetailedText(f"Техническая информация:\n{code}: {message}")
            
        elif error_type == "no_valid_keys":
            dialog.setIcon(QMessageBox.Icon.Critical)
            dialog.setText("🔑 Проблема с доступом к OpenAI")
            dialog.setInformativeText(
                f"Все API ключи недоступны или недействительны.\n\n"
                f"Наиболее вероятные причины:\n"
                f"• OpenAI заблокирован в вашем регионе\n"
                f"• Проблемы с подключением к интернету\n"
                f"• API ключи истекли или недействительны\n\n"
                f"Решение:\n"
                f"1. Включите VPN (если не включен)\n"
                f"2. Проверьте подключение к интернету\n"
                f"3. Перезапустите приложение\n"
                f"4. Обратитесь в поддержку\n\n"
                f"💡 Совет: {suggestion}"
            )
            dialog.setDetailedText(f"Техническая информация:\n{code}: {message}")
            
        else:
            # Общая ошибка
            dialog.setIcon(QMessageBox.Icon.Critical)
            dialog.setText("❌ Произошла ошибка")
            dialog.setInformativeText(
                f"При работе с Hintsage произошла неожиданная ошибка.\n\n"
                f"Попробуйте:\n"
                f"• Перезапустить приложение\n"
                f"• Проверить подключение к интернету\n"
                f"• Обратиться в поддержку\n\n"
                f"💡 Совет: {suggestion}"
            )
            dialog.setDetailedText(f"Техническая информация:\n{code}: {message}")
        
        # Добавляем кнопки
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Показываем диалог
        dialog.exec()
    
    def show_success_message(self, title: str, message: str) -> None:
        """
        Показать сообщение об успехе
        
        Args:
            title: Заголовок сообщения
            message: Текст сообщения
        """
        dialog = QMessageBox(self.parent_widget)
        dialog.setWindowTitle("✅ " + title)
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.setText(message)
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        dialog.exec()
    
    def show_warning_message(self, title: str, message: str) -> None:
        """
        Показать предупреждение
        
        Args:
            title: Заголовок сообщения
            message: Текст сообщения
        """
        dialog = QMessageBox(self.parent_widget)
        dialog.setWindowTitle("⚠️ " + title)
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setText(message)
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        dialog.exec()
    
    def show_info_message(self, title: str, message: str) -> None:
        """
        Показать информационное сообщение
        
        Args:
            title: Заголовок сообщения
            message: Текст сообщения
        """
        dialog = QMessageBox(self.parent_widget)
        dialog.setWindowTitle("ℹ️ " + title)
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.setText(message)
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        dialog.exec()


# Глобальный экземпляр
_error_handler: Optional[ErrorHandler] = None


def get_error_handler(parent_widget: Optional[QWidget] = None) -> ErrorHandler:
    """
    Получить глобальный экземпляр ErrorHandler
    
    Args:
        parent_widget: Родительский виджет для диалогов
        
    Returns:
        ErrorHandler instance
    """
    global _error_handler
    
    if _error_handler is None:
        _error_handler = ErrorHandler(parent_widget)
    elif parent_widget is not None:
        _error_handler.parent_widget = parent_widget
    
    return _error_handler


def handle_api_error(error_message: str, error_code: str = "") -> None:
    """
    Быстрая функция для обработки ошибок API
    
    Args:
        error_message: Сообщение об ошибке
        error_code: Код ошибки
    """
    handler = get_error_handler()
    handler.handle_api_error(error_message, error_code)
