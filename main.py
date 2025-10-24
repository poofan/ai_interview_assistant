"""
Hintsage - AI Interview Assistant
Главное приложение

Архитектура по онтологии "Ясна"
Принцип: Функция = Архетип
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from loguru import logger
import numpy as np
from pathlib import Path
import keyboard  # [ЧЕЛО + ПУТЬ] - глобальные горячие клавиши

# Импорт модулей
from modules.config_manager import ConfigManager
from modules.llm_integration import LLMClient
from modules.context_manager import ContextManager
from modules.audio_capture import AudioCapture
from modules.stt import STTManager
from modules.question_detector import QuestionDetector
from modules.ui_overlay import OverlayWindow
from modules.security import SecurityManager
from modules.screenshot_ocr import ScreenshotManager
from modules.prompt_templates import PromptManager, InterviewProfile
from modules.parallel import RequestQueue
from modules.parallel.utils import format_answer_with_question


class AudioProcessingThread(QThread):
    """
    Поток обработки аудио
    Архетипы: [ИЖЕ + МЫСЛЕТЕ]
    """
    
    text_recognized = pyqtSignal(str)
    
    def __init__(self, audio_capture, stt_manager):
        super().__init__()
        self.audio_capture = audio_capture
        self.stt_manager = stt_manager
        self.running = True
    
    def run(self):
        """Обработка аудиопотока"""
        logger.info("[AUDIO] Поток обработки аудио запущен")
        
        while self.running:
            # Получаем аудио чанк
            audio_chunk = self.audio_capture.get_audio_chunk(timeout=1.0)
            
            if audio_chunk is not None and len(audio_chunk) > 0:
                # Транскрибируем
                text = self.stt_manager.transcribe(audio_chunk)
                
                if text:
                    self.text_recognized.emit(text)
    
    def stop(self):
        """Остановить поток"""
        self.running = False
        logger.info("[STOP] Поток обработки аудио остановлен")


class HintsageApp(QObject):
    """
    Главное приложение Hintsage
    Архетипы: [ДОБРО + ЛАДЪ] - организация и координация
    
    ВАЖНО: Наследуется от QObject для правильной работы Qt сигналов!
    """
    
    def __init__(self, qt_app: QApplication):
        """
        Инициализация приложения
        
        Args:
            qt_app: QApplication instance (должен быть создан ДО HintsageApp!)
        """
        super().__init__()  # [FIX] QObject инициализация для работы сигналов!
        
        logger.info("=" * 60)
        logger.info("[HINTSAGE] Hintsage - AI Interview Assistant")
        logger.info("Архитектура: Онтология 'Ясна'")
        logger.info("=" * 60)
        
        # Qt приложение (передается извне)
        self.qt_app = qt_app
        
        # Инициализация компонентов
        self.config: ConfigManager = None
        self.llm_client: LLMClient = None
        self.context_manager: ContextManager = None
        self.audio_capture: AudioCapture = None
        self.stt_manager: STTManager = None
        self.question_detector: QuestionDetector = None
        self.overlay_window: OverlayWindow = None
        self.security_manager: SecurityManager = None
        self.screenshot_manager: ScreenshotManager = None
        self.prompt_manager: PromptManager = None
        
        # Поток обработки аудио
        self.audio_thread: AudioProcessingThread = None
        
        # Буфер распознанного текста
        self.text_buffer = []
        
        # [ДОБРО + ИЖЕ] Многопоточная обработка
        self.request_queue: RequestQueue = None
        self.answer_buffer = {}  # {request_number: (question, answer)} для сохранения порядка
        self.next_context_number = 1  # Следующий номер для добавления в контекст
        
        self._init_components()
        self._connect_signals()
        self._setup_global_hotkeys()
    
    def _init_components(self) -> None:
        """
        [ДОБРО + ВЕДИ] - Инициализировать все компоненты
        """
        logger.info("Инициализация компонентов...")
        
        # 1. Конфигурация [ДОБРО + АЗ]
        self.config = ConfigManager()
        
        if not self.config.validate_config():
            logger.error("[ERROR] Конфигурация невалидна! Проверьте config.yaml")
            sys.exit(1)
        
        # 2. LLM Client [РЦИ + ИЖЕ]
        api_key = self.config.get_openai_api_key()
        model = self.config.get("openai.model", "gpt-4o")
        max_tokens = self.config.get("openai.max_tokens", 500)
        temperature = self.config.get("openai.temperature", 0.7)
        system_prompt = self.config.get("openai.system_prompt")
        
        self.llm_client = LLMClient(
            api_key=api_key,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system_prompt=system_prompt
        )
        
        # Проверка API ключа
        if not self.llm_client.validate_api_key():
            logger.error("[ERROR] Неверный OpenAI API ключ!")
            sys.exit(1)
        
        # 3. Context Manager [ПАМЯТЬ + ДОБРО]
        self.context_manager = ContextManager(
            max_messages=self.config.get("context.max_messages", 20),
            max_tokens=self.config.get("context.context_window", 4000),
            save_history=self.config.get("context.save_history", True),
            history_path=self.config.get("context.history_path", "data/sessions")
        )
        
        # 4. Audio Capture [ВЕДИ + ИЖЕ]
        self.audio_capture = AudioCapture(
            sample_rate=self.config.get("audio.sample_rate", 16000),
            channels=self.config.get("audio.channels", 1),
            chunk_size=self.config.get("audio.chunk_size", 1024),
            buffer_seconds=self.config.get("audio.buffer_seconds", 30),
            source=self.config.get("audio.source", "microphone")
        )
        
        # 5. STT Manager [МЫСЛЕТЕ + ВЕДИ]
        stt_config = {
            "language": self.config.get("stt.language", "ru"),
            "vosk": self.config.get("stt.vosk", {}),
            "whisper": self.config.get("stt.whisper", {})
        }
        
        self.stt_manager = STTManager(
            default_engine=self.config.get("stt.default_engine", "vosk"),
            config=stt_config
        )
        
        # 6. Question Detector [ЧЕЛО + МЫСЛЕТЕ]
        self.question_detector = QuestionDetector(
            mode=self.config.get("question_detector.mode", "hybrid"),
            confidence_threshold=self.config.get("question_detector.confidence_threshold", 0.7),
            patterns=self.config.get("question_detector.patterns")
        )
        
        # 7. UI Overlay [ЛИЧЬ + ЧЕЛО]
        ui_config = self.config.get("ui.overlay", {})
        
        self.overlay_window = OverlayWindow(
            width=ui_config.get("width", 400),
            height=ui_config.get("height", 600),
            position=ui_config.get("position", "top-right"),
            opacity=ui_config.get("opacity", 0.95),
            phantom_mode=ui_config.get("phantom_mode", True),
            anti_screenshot=self.config.get("security.anti_screenshot", True)
        )
        
        # 8. Security Manager [ШТОР + ТАЙНА]
        self.security_manager = SecurityManager(
            anti_screenshot=self.config.get("security.anti_screenshot", True),
            anti_screen_share=self.config.get("security.anti_screen_share", True),
            no_focus_steal=self.config.get("security.no_focus_steal", True),
            silent_mode=self.config.get("security.silent_mode", True)
        )
        
        # Применяем защиту к overlay окну
        hwnd = int(self.overlay_window.winId())
        self.security_manager.apply_window_protection(hwnd)
        
        # 9. Screenshot Manager [ВЕДИ + МЫСЛЕТЕ]
        screenshot_config = self.config.get("screenshot", {})
        
        self.screenshot_manager = ScreenshotManager(
            ocr_engine=screenshot_config.get("ocr_engine", "easyocr"),
            languages=screenshot_config.get("languages", ["ru", "en"]),
            save_screenshots=screenshot_config.get("save_screenshots", False),
            screenshot_path=screenshot_config.get("screenshot_path", "data/screenshots"),
            gpu=screenshot_config.get("gpu", False)
        )
        
        # 10. Prompt Manager [СЛОВО + ДОБРО]
        default_profile_str = self.config.get("interview.default_profile", "algorithms")
        programming_language = self.config.get("interview.programming_language", "Python")
        auto_detect_language = self.config.get("interview.auto_detect_language", True)
        
        try:
            default_profile = InterviewProfile(default_profile_str)
        except ValueError:
            default_profile = InterviewProfile.ALGORITHMS
            logger.warning(f"Неизвестный профиль '{default_profile_str}', используется 'algorithms'")
        
        self.prompt_manager = PromptManager(
            default_profile=default_profile,
            programming_language=programming_language,
            auto_detect_language=auto_detect_language
        )
        
        # Обновляем системный промпт LLM клиента
        self.llm_client.update_system_prompt(
            self.prompt_manager.get_system_prompt()
        )
        
        # 11. Request Queue [ДОБРО + ИЖЕ] - Многопоточная обработка
        if self.config.get("parallel.enabled", True):
            self.request_queue = RequestQueue(
                max_workers=self.config.get("parallel.max_workers", 3),
                queue_limit=self.config.get("parallel.queue_limit", 10),
                timeout=self.config.get("parallel.timeout", 60)
            )
            logger.info("[OK] RequestQueue инициализирована")
        else:
            logger.info("[INFO] Многопоточная обработка отключена")
        
        logger.info("[OK] Все компоненты инициализированы")
    
    def _setup_global_hotkeys(self) -> None:
        """
        [ЧЕЛО + ПУТЬ] - Настроить глобальные горячие клавиши
        """
        try:
            # Получаем hotkeys из конфига
            hotkeys_config = self.config.get("hotkeys", {})
            
            # Toggle overlay - сворачивание/разворачивание окна
            toggle_key = hotkeys_config.get("toggle_overlay", "ctrl+shift+h")
            keyboard.add_hotkey(toggle_key, self.overlay_window.toggle_window, suppress=True)
            logger.info(f"[HOTKEY] Toggle overlay: {toggle_key}")
            
            # Manual trigger - ручной триггер вопроса
            trigger_key = hotkeys_config.get("manual_trigger", "ctrl+shift+q")
            keyboard.add_hotkey(trigger_key, self._manual_trigger, suppress=True)
            logger.info(f"[HOTKEY] Manual trigger: {trigger_key}")
            
            # Screenshot area - скриншот области
            screenshot_key = hotkeys_config.get("screenshot_area", "ctrl+shift+s")
            keyboard.add_hotkey(screenshot_key, self._trigger_screenshot, suppress=True)
            logger.info(f"[HOTKEY] Screenshot: {screenshot_key}")
            
            # Clear context - очистка контекста
            clear_key = hotkeys_config.get("clear_context", "ctrl+shift+c")
            keyboard.add_hotkey(clear_key, self._clear_context, suppress=True)
            logger.info(f"[HOTKEY] Clear context: {clear_key}")
            
            # Exit - выход из приложения
            exit_key = hotkeys_config.get("exit", "ctrl+shift+x")
            keyboard.add_hotkey(exit_key, self._safe_exit, suppress=True)
            logger.info(f"[HOTKEY] Exit: {exit_key}")
            
            logger.info("[OK] Глобальные горячие клавиши зарегистрированы")
            
        except Exception as e:
            logger.error(f"[ERROR] Ошибка регистрации hotkeys: {e}")
    
    def _manual_trigger(self) -> None:
        """[ЧЕЛО] - Ручной триггер вопроса"""
        self.overlay_window.trigger_question.emit()
    
    def _trigger_screenshot(self) -> None:
        """[ВЕДИ] - Триггер скриншота"""
        self.overlay_window.take_screenshot.emit()
    
    def _clear_context(self) -> None:
        """[ПАМЯТЬ] - Очистка контекста"""
        self.overlay_window.clear_context.emit()
    
    def _safe_exit(self) -> None:
        """[НАВЬ] - Безопасный выход"""
        logger.info("[EXIT] Выход по горячей клавише")
        self.qt_app.quit()
    
    def _connect_signals(self) -> None:
        """
        [ИЖЕ + ЧЕЛО] - Подключить сигналы
        """
        # Сигналы от UI
        self.overlay_window.trigger_question.connect(self._manual_trigger)
        self.overlay_window.clear_context.connect(self._clear_context)
        self.overlay_window.take_screenshot.connect(self._take_screenshot)
    
    def _on_text_recognized(self, text: str) -> None:
        """
        [МЫСЛЕТЕ + ЧЕЛО] - Обработка распознанного текста
        
        Args:
            text: Распознанный текст
        """
        logger.info(f"[TEXT] Распознано: {text}")
        
        # Добавляем в буфер
        self.text_buffer.append(text)
        
        # Объединяем последние несколько фраз
        recent_text = " ".join(self.text_buffer[-5:])
        
        # Проверяем, является ли вопросом
        if self.question_detector.should_trigger(text):
            self._generate_answer(recent_text)
    
    def _manual_trigger(self) -> None:
        """
        [ЧЕЛО + ЖИВЕТЕ + ДОБРО] - Ручной триггер генерации ответа (ASYNC)
        
        Новая версия с многопоточной обработкой:
        - Добавляет запрос в очередь (не блокирует UI)
        - Позволяет нажимать триггер несколько раз подряд
        - Показывает ответы по мере готовности (Completion Order)
        """
        logger.info("[TRIGGER] Ручной триггер активирован")
        
        # Берем последние несколько секунд аудио
        audio_buffer = self.audio_capture.get_buffer(seconds=10)
        
        # [ШТОР + НАВЬ] - Валидация буфера
        if audio_buffer is None or len(audio_buffer) == 0:
            logger.warning("[WARNING] Аудио буфер пуст - аудиозахват не активен")
            self.overlay_window.show_error("Аудиозахват не активен. Проверьте микрофон.")
            return
        
        # Проверка на тишину (все близко к 0)
        if np.max(np.abs(audio_buffer)) < 0.001:
            logger.warning("[WARNING] Аудио буфер содержит только тишину")
            self.overlay_window.show_error("Тишина в аудио. Говорите в микрофон!")
            return
        
        # [ДОБРО + ИЖЕ] - Отправляем в очередь (НЕ БЛОКИРУЕТ!)
        if self.request_queue and self.config.get("parallel.enabled", True):
            try:
                # [FIX] Передаем callbacks напрямую в submit
                request_id, request_number = self.request_queue.submit(
                    audio_buffer=audio_buffer,
                    stt_manager=self.stt_manager,
                    llm_client=self.llm_client,
                    prompt_manager=self.prompt_manager,
                    context_manager=self.context_manager,
                    request_type="manual",
                    # Подключаем обработчики ДО запуска задачи
                    on_started=self._on_request_started,
                    on_progress=self._on_request_progress,
                    on_finished=self._on_request_finished,
                    on_error=self._on_request_error
                )
                
                logger.info(f"[QUEUE] Запрос #{request_number} добавлен в очередь (ID: {request_id})")
                self.overlay_window.set_status(f"⏳ Запрос #{request_number} в очереди", "#ffaa00")
                
                # СРАЗУ готовы к новому триггеру! 🚀
                
            except Exception as e:
                logger.error(f"[ERROR] Ошибка добавления в очередь: {e}")
                self.overlay_window.show_error(f"Очередь переполнена: {e}")
        else:
            # Fallback на старый синхронный метод
            self.overlay_window.set_status("[WAIT] Распознавание речи...", "#ffaa00")
            text = self.stt_manager.transcribe(audio_buffer)
            
            if text:
                logger.info(f"[TEXT] Распознано (ручной триггер): {text}")
                self._generate_answer(text)
            else:
                self.overlay_window.show_error("Не удалось распознать речь")
    
    def _generate_answer(self, question: str) -> None:
        """
        [РЦИ + МЫСЛЕТЕ] - Генерация ответа
        
        Args:
            question: Вопрос
        """
        logger.info(f"[THINKING] Генерация ответа на: {question[:100]}...")
        
        # УЛУЧШЕНИЕ: Определяем тип вопроса и улучшаем его
        detected_profile = self.prompt_manager.detect_question_type(question)
        enhanced_question = self.prompt_manager.enhance_question(question, detected_profile)
        
        # ВСЕГДА обновляем системный промпт для текущего вопроса
        system_prompt = self.prompt_manager.get_system_prompt(detected_profile)
        self.llm_client.update_system_prompt(system_prompt)
        
        logger.info(f"[INFO] Профиль для этого вопроса: {detected_profile.value}")
        logger.debug(f"[DEBUG] Улучшенный вопрос: {enhanced_question[:200]}...")
        
        # Добавляем ИСХОДНЫЙ вопрос в контекст (для истории)
        self.context_manager.add_user_message(question)
        
        # [ПАМЯТЬ + ДОБРО] - Умное управление контекстом
        if detected_profile != self.prompt_manager.current_profile:
            logger.info(f"[INFO] Смена профиля: {self.prompt_manager.current_profile.value} -> {detected_profile.value}")
            # При смене профиля сохраняем больше контекста для связности
            context = self.context_manager.get_recent_context(n_messages=6)
            self.prompt_manager.current_profile = detected_profile
        else:
            # [ПАМЯТЬ] - Полный контекст для того же профиля (последние 10 сообщений)
            context = self.context_manager.get_recent_context(n_messages=10)
        
        # Показываем индикатор загрузки
        self.overlay_window.show_loading()
        
        try:
            # Генерируем ответ с УЛУЧШЕННЫМ вопросом
            answer = self.llm_client.generate_response(enhanced_question, context)
            
            # Добавляем ответ в контекст
            self.context_manager.add_assistant_message(answer)
            
            # [ЛИЧЬ + ПАМЯТЬ] - Форматированный вывод с контекстом
            message_count = len(self.context_manager) // 2  # Пары вопрос-ответ
            formatted_answer = f"[Q{message_count}] {question}\n\n💡 {answer}"
            
            # Отображаем ответ (режим из конфига)
            accumulate = self.config.get("ui.accumulate_answers", True)
            self.overlay_window.display_answer(formatted_answer, append_mode=accumulate)
            
            # [ПАМЯТЬ] - Обновляем индикатор контекста
            context_size = len(self.context_manager)
            self.overlay_window.update_context_indicator(context_size)
            
            logger.info(f"[OK] Ответ сгенерирован ({len(answer)} символов, профиль: {detected_profile.value}, контекст: {context_size} сообщений)")
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка генерации ответа: {e}")
            self.overlay_window.show_error(str(e))
    
    def _clear_context(self) -> None:
        """
        [ПАМЯТЬ] - Очистить контекст
        """
        self.context_manager.clear_context()
        self.text_buffer.clear()
        
        # [ЛИЧЬ] - Обновляем индикатор
        self.overlay_window.update_context_indicator(0)
        
        logger.info("[CLEAR] Контекст очищен")
    
    def _on_request_started(self, request_id: str, request_number: int):
        """
        [ДОБРО + ИЖЕ] - Обработчик начала запроса
        """
        try:
            logger.info(f"[HANDLER STARTED] Вызван для #{request_number} (ID: {request_id})")
            logger.info(f"[TASK {request_number}] Начат (ID: {request_id})")
            self.overlay_window.set_status(f"🔄 Запрос #{request_number} обрабатывается", "#ffaa00")
        except Exception as e:
            logger.error(f"[ERROR] Ошибка в _on_request_started: {e}", exc_info=True)
    
    def _on_request_progress(self, request_id: str, request_number: int, stage: str):
        """
        [ДОБРО + ИЖЕ] - Обработчик прогресса запроса
        """
        stage_names = {
            "STT": "🎙️ Распознавание речи",
            "LLM": "🤖 Генерация ответа"
        }
        stage_name = stage_names.get(stage, stage)
        logger.debug(f"[TASK {request_number}] {stage_name}")
        self.overlay_window.set_status(f"{stage_name} (запрос #{request_number})", "#ffaa00")
    
    def _on_request_finished(self, request_id: str, request_number: int, question: str, answer: str):
        """
        [ДОБРО + ИЖЕ + COMPLETION ORDER] - Обработчик завершения запроса
        
        Ключевой метод для Completion Order:
        - Отображает ответ СРАЗУ (по мере готовности)
        - Добавляет в контекст в правильном порядке (через буфер)
        """
        try:
            logger.info(f"[HANDLER FINISHED] ★★★ ВЫЗВАН ДЛЯ #{request_number} (ID: {request_id}) ★★★")
            logger.info(f"[TASK {request_number}] Завершен (вопрос: {question[:50]}...)")
            
            # [COMPLETION ORDER] Добавляем в буфер с номером
            self.answer_buffer[request_number] = (question, answer)
            
            # Добавляем в контекст все готовые ответы по порядку
            while self.next_context_number in self.answer_buffer:
                q, a = self.answer_buffer.pop(self.next_context_number)
                self.context_manager.add_user_message(q)
                self.context_manager.add_assistant_message(a)
                self.next_context_number += 1
                logger.debug(f"[CONTEXT] Добавлен запрос #{self.next_context_number - 1} в контекст")
            
            # [ЛИЧЬ + СЛОВО] Отображаем ответ СРАЗУ (Completion Order для UI)
            show_question = self.config.get("parallel.show_question_in_answer", True)
            question_max_length = self.config.get("parallel.question_max_length", 100)
            
            formatted_answer = format_answer_with_question(
                request_number=request_number,
                question=question,
                answer=answer,
                show_question=show_question,
                question_max_length=question_max_length
            )
            
            # Отображаем в накопительном режиме
            accumulate = self.config.get("ui.accumulate_answers", True)
            self.overlay_window.display_answer(formatted_answer, append_mode=accumulate)
            
            # Обновляем индикатор контекста
            context_size = len(self.context_manager)
            self.overlay_window.update_context_indicator(context_size)
            
            # Удаляем из активных запросов
            self.request_queue.remove_request(request_id)
            
            # Обновляем статус
            active_count = self.request_queue.get_active_count()
            if active_count > 0:
                self.overlay_window.set_status(f"✅ Готово #{request_number} | Активно: {active_count}", "#00ff00")
            else:
                self.overlay_window.set_status("✅ Все запросы обработаны", "#00ff00")
            
            logger.info(f"[OK] Ответ #{request_number} отображен (контекст: {context_size} сообщений)")
            
        except Exception as e:
            logger.error(f"[ERROR] Ошибка в _on_request_finished для #{request_number}: {e}", exc_info=True)
    
    def _on_request_error(self, request_id: str, request_number: int, error_msg: str):
        """
        [ДОБРО + НАВЬ] - Обработчик ошибки запроса
        """
        logger.error(f"[TASK {request_number}] Ошибка: {error_msg}")
        
        # Отображаем ошибку
        error_text = f"[Q{request_number}] ❌ Ошибка\n\n{error_msg}"
        self.overlay_window.display_answer(error_text, append_mode=True)
        
        # Удаляем из активных
        self.request_queue.remove_request(request_id)
        
        # Обновляем статус
        active_count = self.request_queue.get_active_count()
        self.overlay_window.set_status(f"❌ Ошибка #{request_number} | Активно: {active_count}", "#ff0000")
    
    def _take_screenshot(self) -> None:
        """
        [ВЕДИ + МЫСЛЕТЕ] - Сделать скриншот и распознать текст
        """
        logger.info("[SCREENSHOT] Захват скриншота...")
        
        self.overlay_window.set_status("[SCREENSHOT] Захват скриншота...", "#ffaa00")
        
        # Захватываем весь экран (можно улучшить до выбора области)
        text = self.screenshot_manager.capture_and_ocr()
        
        if text:
            logger.info(f"[OK] Текст распознан: {text[:100]}...")
            
            # УЛУЧШЕНИЕ: Формируем запрос в зависимости от содержимого
            # Определяем язык из скриншота
            detected_lang = self.prompt_manager.detect_language(text)
            language = detected_lang or self.prompt_manager.programming_language
            
            # Проверяем, похоже ли на задачу
            if any(keyword in text.lower() for keyword in ['function', 'def', 'задача', 'реализ', 'напиш', 'алгоритм', 'implement', 'write']):
                # Это похоже на задачу - просим решение
                question = f"""На скриншоте задача:

{text}

Дай ГОТОВОЕ РЕШЕНИЕ с кодом на {language}. Включи комментарии и объяснение."""
            else:
                # Обычный текст - просим объяснение
                question = f"Объясни следующее: {text}"
            
            # Генерируем ответ
            self._generate_answer(question)
        else:
            self.overlay_window.show_error("Не удалось распознать текст на скриншоте")
    
    def start(self) -> None:
        """
        [ЖИВЕТЕ + ИЖЕ] - Запустить приложение
        """
        logger.info("[START] Запуск Hintsage...")
        
        # Запускаем аудиозахват
        try:
            self.audio_capture.start()
            
            # Запускаем поток обработки аудио
            self.audio_thread = AudioProcessingThread(self.audio_capture, self.stt_manager)
            self.audio_thread.text_recognized.connect(self._on_text_recognized)
            self.audio_thread.start()
        except Exception as e:
            logger.error(f"Ошибка запуска аудиозахвата: {e}")
            logger.warning("Приложение запущено БЕЗ аудиозахвата (можно использовать только ручной режим)")
        
        # Показываем overlay
        self.overlay_window.show()
        self.overlay_window.set_status("[OK] Готов к работе", "#00ff00")
        
        logger.info("[OK] Hintsage запущен!")
        logger.info("Горячие клавиши:")
        logger.info("  - Ctrl+Shift+Q: Ручной триггер")
        logger.info("  - Ctrl+Shift+S: Скриншот")
        logger.info("  - Esc: Скрыть окно")
        
        # Запускаем Qt event loop
        sys.exit(self.qt_app.exec())
    
    def shutdown(self) -> None:
        """
        [НАВЬ] - Завершение работы
        """
        logger.info("[STOP] Завершение работы...")
        
        # Отключаем глобальные hotkeys [ЧЕЛО + ПУТЬ]
        try:
            keyboard.unhook_all()
            logger.info("[OK] Глобальные hotkeys отключены")
        except Exception as e:
            logger.warning(f"Ошибка отключения hotkeys: {e}")
        
        # Останавливаем поток
        if self.audio_thread:
            self.audio_thread.stop()
            self.audio_thread.wait()
        
        # Останавливаем аудиозахват
        if self.audio_capture:
            self.audio_capture.stop()
        
        # Сохраняем сессию
        if self.context_manager and len(self.context_manager) > 0:
            self.context_manager.save_session()
            
            # Экспорт в Markdown
            if self.config.get("context.export_format") == "markdown":
                self.context_manager.export_to_markdown()
        
        logger.info("[BYE] Hintsage завершен")


def main():
    """
    Точка входа
    """
    # [ДИАГНОСТ] Настройка кодировки для Windows
    import locale
    import io
    
    # Устанавливаем UTF-8 для stdout
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    # Настройка логирования
    logger.remove()
    
    # Консольный вывод с UTF-8 (для русского языка)
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>"
    )
    
    # Файловый вывод с полной информацией (UTF-8 по умолчанию)
    logger.add(
        "logs/hintsage.log",
        rotation="1 day",
        retention="7 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
    )
    
    # [FIX] Создаем QApplication ДО создания HintsageApp (для правильной работы QObject сигналов!)
    qt_app = QApplication(sys.argv)
    
    # Создаем и запускаем приложение
    app = HintsageApp(qt_app)
    
    try:
        app.start()
    except KeyboardInterrupt:
        logger.info("Прервано пользователем")
    finally:
        app.shutdown()


if __name__ == "__main__":
    main()

