"""
Тестовый скрипт для проверки всех модулей Hintsage
Запуск: python test_modules.py
"""

import sys
from loguru import logger

# Настройка логирования
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
)


def test_imports():
    """Тест импортов всех модулей"""
    logger.info("=== Тест 1: Импорт модулей ===")
    
    try:
        from modules.config_manager import ConfigManager
        logger.info("✅ config_manager")
    except Exception as e:
        logger.error(f"❌ config_manager: {e}")
    
    try:
        from modules.llm_integration import LLMClient
        logger.info("✅ llm_integration")
    except Exception as e:
        logger.error(f"❌ llm_integration: {e}")
    
    try:
        from modules.context_manager import ContextManager
        logger.info("✅ context_manager")
    except Exception as e:
        logger.error(f"❌ context_manager: {e}")
    
    try:
        from modules.audio_capture import AudioCapture
        logger.info("✅ audio_capture")
    except Exception as e:
        logger.error(f"❌ audio_capture: {e}")
    
    try:
        from modules.stt import STTManager
        logger.info("✅ stt")
    except Exception as e:
        logger.error(f"❌ stt: {e}")
    
    try:
        from modules.question_detector import QuestionDetector
        logger.info("✅ question_detector")
    except Exception as e:
        logger.error(f"❌ question_detector: {e}")
    
    try:
        from modules.ui_overlay import OverlayWindow
        logger.info("✅ ui_overlay")
    except Exception as e:
        logger.error(f"❌ ui_overlay: {e}")
    
    try:
        from modules.security import SecurityManager
        logger.info("✅ security")
    except Exception as e:
        logger.error(f"❌ security: {e}")
    
    try:
        from modules.screenshot_ocr import ScreenshotManager
        logger.info("✅ screenshot_ocr")
    except Exception as e:
        logger.error(f"❌ screenshot_ocr: {e}")


def test_config():
    """Тест менеджера конфигурации"""
    logger.info("\n=== Тест 2: ConfigManager ===")
    
    try:
        from modules.config_manager import ConfigManager
        
        config = ConfigManager()
        
        # Тест чтения
        model = config.get("openai.model", "gpt-4")
        logger.info(f"✅ Чтение конфигурации: модель = {model}")
        
        # Тест установки
        config.set("test.key", "test_value")
        value = config.get("test.key")
        assert value == "test_value"
        logger.info(f"✅ Установка значений работает")
        
        # Тест шифрования
        encrypted = config.encrypt_api_key("test-api-key")
        decrypted = config.decrypt_api_key(encrypted)
        assert decrypted == "test-api-key"
        logger.info(f"✅ Шифрование/расшифровка работает")
        
    except Exception as e:
        logger.error(f"❌ ConfigManager: {e}")


def test_context():
    """Тест менеджера контекста"""
    logger.info("\n=== Тест 3: ContextManager ===")
    
    try:
        from modules.context_manager import ContextManager
        
        context = ContextManager(save_history=False)
        
        # Добавляем сообщения
        context.add_user_message("Привет!")
        context.add_assistant_message("Здравствуйте!")
        
        # Проверяем
        messages = context.get_context()
        assert len(messages) == 2
        logger.info(f"✅ Добавление сообщений: {len(messages)} сообщений")
        
        # Статистика
        stats = context.get_statistics()
        logger.info(f"✅ Статистика: {stats['total_messages']} сообщений")
        
    except Exception as e:
        logger.error(f"❌ ContextManager: {e}")


def test_question_detector():
    """Тест детектора вопросов"""
    logger.info("\n=== Тест 4: QuestionDetector ===")
    
    try:
        from modules.question_detector import QuestionDetector
        
        detector = QuestionDetector(mode="regex")
        
        # Тест вопросов
        test_cases = [
            ("Что такое Python?", True),
            ("Как работает GIL?", True),
            ("Это просто утверждение", False),
            ("Почему небо голубое?", True),
            ("Расскажи про ООП", True),
        ]
        
        passed = 0
        for text, expected in test_cases:
            is_q, conf = detector.is_question(text)
            if is_q == expected:
                passed += 1
                logger.info(f"✅ '{text}' -> {is_q} (conf: {conf:.2f})")
            else:
                logger.warning(f"⚠️ '{text}' -> {is_q}, ожидалось {expected}")
        
        logger.info(f"✅ Пройдено {passed}/{len(test_cases)} тестов")
        
    except Exception as e:
        logger.error(f"❌ QuestionDetector: {e}")


def test_syntax_highlighter():
    """Тест подсветки синтаксиса"""
    logger.info("\n=== Тест 5: SyntaxHighlighter ===")
    
    try:
        from modules.syntax_highlighter import SyntaxHighlighter
        
        highlighter = SyntaxHighlighter()
        
        # Тест подсветки кода
        code = "def hello():\n    print('Hello, World!')"
        html = highlighter.highlight_code(code, "python")
        
        assert len(html) > 0
        assert "hello" in html
        logger.info(f"✅ Подсветка кода работает ({len(html)} символов HTML)")
        
        # Тест Markdown
        markdown_text = "# Заголовок\n\n```python\nprint('test')\n```"
        result = highlighter.process_markdown(markdown_text)
        logger.info(f"✅ Обработка Markdown работает")
        
    except Exception as e:
        logger.error(f"❌ SyntaxHighlighter: {e}")


def test_security():
    """Тест менеджера безопасности"""
    logger.info("\n=== Тест 6: SecurityManager ===")
    
    try:
        from modules.security import SecurityManager
        
        security = SecurityManager()
        
        # Получаем статус
        status = security.get_security_status()
        logger.info(f"✅ Платформа: {status['platform']}")
        logger.info(f"✅ Поддержка: {status['platform_supported']}")
        
        if status['platform_supported']:
            logger.info(f"✅ Антидетект доступен на этой платформе")
        else:
            logger.warning(f"⚠️ Антидетект не поддерживается на {status['platform']}")
        
    except Exception as e:
        logger.error(f"❌ SecurityManager: {e}")


def main():
    """Главная функция"""
    logger.info("🧠 Hintsage - Тестирование модулей\n")
    
    test_imports()
    test_config()
    test_context()
    test_question_detector()
    test_syntax_highlighter()
    test_security()
    
    logger.info("\n" + "=" * 50)
    logger.info("✅ Тестирование завершено!")
    logger.info("=" * 50)
    logger.info("\nДля полноценного теста запустите: python main.py")


if __name__ == "__main__":
    main()


