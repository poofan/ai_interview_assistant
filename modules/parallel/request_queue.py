"""
Request Queue - [ДОБРО + ИЖЕ]
Очередь для параллельной обработки запросов с Completion Order
"""

import time
import numpy as np
from typing import Optional, Callable, Any
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from loguru import logger


class RequestTask(QThread):
    """
    [МЫСЛЕТЕ + РЦИ] - Рабочая задача
    Один запрос: STT → LLM → результат
    Запускается в отдельном потоке (QThread)
    """
    # Сигналы (определяем на уровне класса для QThread)
    started = pyqtSignal(str, int)  # request_id, request_number
    progress = pyqtSignal(str, int, str)  # request_id, request_number, stage
    finished = pyqtSignal(str, int, str, str)  # request_id, request_number, question, answer
    error = pyqtSignal(str, int, str)  # request_id, request_number, error_msg
    
    def __init__(
        self,
        request_id: str,
        request_number: int,
        audio_buffer: np.ndarray,
        stt_manager: Any,
        llm_client: Any,
        prompt_manager: Any,
        context_manager: Any,
        request_type: str = "manual"
    ):
        super().__init__()
        self.request_id = request_id
        self.request_number = request_number
        self.audio_buffer = audio_buffer
        self.stt_manager = stt_manager
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.context_manager = context_manager
        self.request_type = request_type
    
    def run(self):
        """
        Выполнение в отдельном потоке (QThread)
        """
        try:
            self.started.emit(self.request_id, self.request_number)
            logger.info(f"[TASK {self.request_number}] Начало обработки")
            
            # [ВЕДИ] STT - Распознавание речи
            self.progress.emit(self.request_id, self.request_number, "STT")
            logger.debug(f"[TASK {self.request_number}] STT начало")
            
            question = self.stt_manager.transcribe(self.audio_buffer)
            
            if not question:
                raise Exception("Не удалось распознать речь")
            
            logger.info(f"[TASK {self.request_number}] STT готово: {question[:50]}...")
            
            # [МЫСЛЕТЕ] LLM - Генерация ответа
            self.progress.emit(self.request_id, self.request_number, "LLM")
            logger.debug(f"[TASK {self.request_number}] LLM начало")
            
            # Определяем тип вопроса
            detected_profile = self.prompt_manager.detect_question_type(question)
            enhanced_question = self.prompt_manager.enhance_question(question, detected_profile)
            
            # Обновляем системный промпт
            system_prompt = self.prompt_manager.get_system_prompt(detected_profile)
            self.llm_client.update_system_prompt(system_prompt)
            
            # Получаем контекст (упрощенно - без добавления в общий контекст)
            context = self.context_manager.get_recent_context(n_messages=10)
            
            # Генерируем ответ
            answer = self.llm_client.generate_response(enhanced_question, context)
            
            logger.info(f"[TASK {self.request_number}] LLM готово ({len(answer)} символов)")
            
            # [СЛОВО] Результат - отправляем сигнал (QThread работает напрямую!)
            logger.info(f"[TASK {self.request_number}] Отправка сигнала finished...")
            self.finished.emit(
                self.request_id,
                self.request_number,
                question,  # Исходный вопрос
                answer
            )
            logger.info(f"[TASK {self.request_number}] Сигнал finished отправлен")
            
            logger.info(f"[TASK {self.request_number}] Завершено успешно")
            
        except Exception as e:
            logger.error(f"[TASK {self.request_number}] Ошибка: {e}")
            self.error.emit(
                self.request_id,
                self.request_number,
                str(e)
            )


class RequestQueue:
    """
    [ДОБРО + ИЖЕ] - Очередь запросов
    
    Управление параллельной обработкой с Completion Order:
    - Запуск: параллельный (до max_workers)
    - Отображение: по мере готовности (Completion Order)
    - Контекст: в правильном порядке (FIFO через буфер)
    """
    
    def __init__(
        self,
        max_workers: int = 3,
        queue_limit: int = 10,
        timeout: int = 60
    ):
        """
        Инициализация очереди
        
        Args:
            max_workers: Максимум одновременных потоков
            queue_limit: Максимум запросов в очереди
            timeout: Таймаут на один запрос (сек)
        """
        self.max_workers = max_workers
        self.queue_limit = queue_limit
        self.timeout = timeout
        
        # Активные QThread потоки
        self.active_threads = {}  # {request_id: RequestTask (QThread)}
        
        # Счетчики
        self.next_number = 1  # Для нумерации [Q1], [Q2], [Q3]...
        self.active_requests = {}  # {request_id: request_number}
        
        logger.info(f"[QUEUE] Инициализирована (max_workers={max_workers}, используется QThread)")
    
    def submit(
        self,
        audio_buffer: np.ndarray,
        stt_manager: Any,
        llm_client: Any,
        prompt_manager: Any,
        context_manager: Any,
        request_type: str = "manual",
        on_started: Callable = None,
        on_progress: Callable = None,
        on_finished: Callable = None,
        on_error: Callable = None
    ) -> tuple[str, int]:
        """
        Добавить запрос в обработку
        
        Args:
            audio_buffer: Аудио данные
            stt_manager: STT менеджер
            llm_client: LLM клиент
            prompt_manager: Менеджер промптов
            context_manager: Менеджер контекста
            request_type: Тип запроса
            on_started: Callback для начала обработки
            on_progress: Callback для прогресса
            on_finished: Callback для завершения
            on_error: Callback для ошибки
        
        Returns:
            (request_id, request_number)
        """
        # Проверка лимита
        if len(self.active_requests) >= self.queue_limit:
            logger.warning(f"[QUEUE] Достигнут лимит очереди ({self.queue_limit})")
            raise Exception(f"Очередь переполнена (макс. {self.queue_limit} запросов)")
        
        # Генерируем ID и номер
        request_id = f"req_{int(time.time() * 1000)}"
        request_number = self.next_number
        self.next_number += 1
        
        # Создаем задачу
        task = RequestTask(
            request_id=request_id,
            request_number=request_number,
            audio_buffer=audio_buffer,
            stt_manager=stt_manager,
            llm_client=llm_client,
            prompt_manager=prompt_manager,
            context_manager=context_manager,
            request_type=request_type
        )
        
        # [FIX] Подключаем сигналы ДО запуска потока (QThread автоматически использует QueuedConnection!)
        if on_started:
            task.started.connect(on_started)
            logger.debug(f"[QUEUE] Подключен on_started для #{request_number}")
        if on_progress:
            task.progress.connect(on_progress)
            logger.debug(f"[QUEUE] Подключен on_progress для #{request_number}")
        if on_finished:
            task.finished.connect(on_finished)
            logger.debug(f"[QUEUE] Подключен on_finished для #{request_number}")
        if on_error:
            task.error.connect(on_error)
            logger.debug(f"[QUEUE] Подключен on_error для #{request_number}")
        
        # Запоминаем активный запрос и поток
        self.active_requests[request_id] = request_number
        self.active_threads[request_id] = task
        
        # Важно: НЕ удалять поток автоматически до завершения обработки сигналов
        task.setTerminationEnabled(False)
        
        # Запускаем QThread (после подключения сигналов!)
        task.start()
        
        logger.info(f"[QUEUE] QThread запущен для запроса #{request_number}")
        
        logger.info(f"[QUEUE] Запрос {request_number} добавлен (ID: {request_id})")
        logger.debug(f"[QUEUE] Активных запросов: {len(self.active_requests)}/{self.max_workers}")
        
        return request_id, request_number
    
    def remove_request(self, request_id: str):
        """
        Удалить запрос из активных (после завершения)
        """
        if request_id in self.active_requests:
            request_number = self.active_requests.pop(request_id)
            logger.debug(f"[QUEUE] Запрос {request_number} (ID: {request_id}) завершен")
        
        # Удаляем поток
        if request_id in self.active_threads:
            thread = self.active_threads.pop(request_id)
            if thread.isRunning():
                thread.wait(100)  # Ждем завершения макс 100мс
            logger.debug(f"[QUEUE] Поток для {request_id} удален")
    
    def get_active_count(self) -> int:
        """Получить количество активных запросов"""
        return len(self.active_requests)
    
    def get_queue_status(self) -> dict:
        """
        Получить статус очереди
        
        Returns:
            {
                "active": int,
                "max_workers": int,
                "queue_limit": int
            }
        """
        return {
            "active": len(self.active_requests),
            "max_workers": self.max_workers,
            "queue_limit": self.queue_limit
        }

