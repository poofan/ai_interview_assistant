"""
Тест Error Handler - демонстрация GUI уведомлений
"""

import sys
from PyQt6.QtWidgets import QApplication
from modules.ui.error_handler import get_error_handler

def test_error_handler():
    """Тестируем Error Handler с разными типами ошибок"""
    
    # Создаем QApplication
    app = QApplication(sys.argv)
    
    # Получаем Error Handler
    error_handler = get_error_handler()
    
    print("🧪 Тестируем Error Handler...")
    print("1. Тест ошибки VPN (unsupported_country)")
    error_handler.handle_api_error(
        "Country, region, or territory not supported",
        "unsupported_country_region_territory"
    )
    
    print("2. Тест ошибки API ключа")
    error_handler.handle_api_error(
        "Invalid API key provided",
        "invalid_api_key"
    )
    
    print("3. Тест информационного сообщения")
    error_handler.show_info_message(
        "Тест завершен",
        "Все тесты Error Handler выполнены успешно!"
    )
    
    print("✅ Тесты завершены!")
    sys.exit(0)

if __name__ == "__main__":
    test_error_handler()
