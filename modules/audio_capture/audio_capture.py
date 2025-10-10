"""
Audio Capture - [ВЕДИ + ИЖЕ]
Непрерывный захват аудиопотока
"""

import sounddevice as sd
import numpy as np
from queue import Queue
from threading import Thread, Event
from typing import Optional, Callable
from loguru import logger
import time


class AudioCapture:
    """
    Модуль захвата аудио
    Архетипы:
    - ВЕДИ: получение аудиоданных
    - ИЖЕ: непрерывный поток
    - ЖИВЕТЕ: жизненный цикл записи
    """
    
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024,
        buffer_seconds: int = 30,
        source: str = "microphone"
    ):
        """
        Инициализация аудиозахвата
        
        Args:
            sample_rate: Частота дискретизации (Hz)
            channels: Количество каналов (1 - моно, 2 - стерео)
            chunk_size: Размер чанка
            buffer_seconds: Размер буфера в секундах
            source: Источник аудио (microphone, system или both)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.buffer_seconds = buffer_seconds
        self.source = source
        
        # Буфер для аудио
        self.buffer_size = int(sample_rate * buffer_seconds)
        self.audio_queue = Queue()
        self.audio_buffer = np.zeros(self.buffer_size, dtype=np.float32)
        self.buffer_position = 0
        
        # Управление потоком
        self.is_recording = Event()
        self.recording_thread: Optional[Thread] = None
        self.stream: Optional[sd.InputStream] = None
        
        # Callback для обработки аудио
        self.audio_callback: Optional[Callable] = None
        
        logger.info(f"[OK] AudioCapture инициализирован ({source}, {sample_rate}Hz)")
    
    def start(self) -> None:
        """
        [ЖИВЕТЕ + ИЖЕ] - Начать захват аудио
        """
        if self.is_recording.is_set():
            logger.warning("Захват аудио уже запущен")
            return
        
        self.is_recording.set()
        
        try:
            # Определяем устройство
            device = self._get_audio_device()
            
            # Создаем поток
            self.stream = sd.InputStream(
                device=device,
                samplerate=self.sample_rate,
                channels=self.channels,
                blocksize=self.chunk_size,
                callback=self._audio_callback
            )
            
            self.stream.start()
            
            logger.info(f"[AUDIO] Захват аудио запущен (устройство: {device})")
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка запуска захвата аудио: {e}")
            self.is_recording.clear()
            raise
    
    def stop(self) -> None:
        """
        [ЖИВЕТЕ] - Остановить захват аудио
        """
        if not self.is_recording.is_set():
            logger.warning("Захват аудио не запущен")
            return
        
        self.is_recording.clear()
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        logger.info("[STOP] Захват аудио остановлен")
    
    def _audio_callback(self, indata, frames, time_info, status):
        """
        [ИЖЕ + ВЕДИ] - Callback для обработки аудиопотока
        
        Args:
            indata: Входные аудиоданные
            frames: Количество фреймов
            time_info: Информация о времени
            status: Статус потока
        """
        if status:
            logger.warning(f"Статус аудиопотока: {status}")
        
        # Преобразуем в mono если нужно
        audio_data = indata[:, 0] if self.channels == 2 else indata.flatten()
        
        # Добавляем в очередь
        self.audio_queue.put(audio_data.copy())
        
        # Добавляем в кольцевой буфер
        self._add_to_buffer(audio_data)
        
        # Вызываем пользовательский callback если есть
        if self.audio_callback:
            try:
                self.audio_callback(audio_data)
            except Exception as e:
                logger.error(f"Ошибка в audio_callback: {e}")
    
    def _add_to_buffer(self, audio_data: np.ndarray) -> None:
        """
        [ПАМЯТЬ + ИЖЕ] - Добавить данные в кольцевой буфер
        
        Args:
            audio_data: Аудиоданные для добавления
        """
        data_len = len(audio_data)
        
        if self.buffer_position + data_len <= self.buffer_size:
            # Вмещается без перезаписи
            self.audio_buffer[self.buffer_position:self.buffer_position + data_len] = audio_data
            self.buffer_position += data_len
        else:
            # Переполнение - циклический буфер
            overflow = (self.buffer_position + data_len) - self.buffer_size
            
            # Записываем до конца
            self.audio_buffer[self.buffer_position:] = audio_data[:self.buffer_size - self.buffer_position]
            
            # Записываем в начало
            self.audio_buffer[:overflow] = audio_data[self.buffer_size - self.buffer_position:]
            
            self.buffer_position = overflow
    
    def get_audio_chunk(self, timeout: float = 1.0) -> Optional[np.ndarray]:
        """
        [ВЕДИ] - Получить чанк аудио из очереди
        
        Args:
            timeout: Таймаут ожидания
        
        Returns:
            Массив аудиоданных или None
        """
        try:
            return self.audio_queue.get(timeout=timeout)
        except:
            return None
    
    def get_buffer(self, seconds: Optional[int] = None) -> np.ndarray:
        """
        [ПАМЯТЬ + ВЕДИ] - Получить аудио из буфера
        
        Args:
            seconds: Сколько секунд взять (None - весь буфер)
        
        Returns:
            Аудиоданные из буфера
        """
        if seconds is None:
            return self.audio_buffer.copy()
        
        samples = int(self.sample_rate * seconds)
        samples = min(samples, self.buffer_size)
        
        # Берем последние N сэмплов
        if self.buffer_position >= samples:
            return self.audio_buffer[self.buffer_position - samples:self.buffer_position].copy()
        else:
            # Циклический буфер
            part1 = self.audio_buffer[self.buffer_size - (samples - self.buffer_position):]
            part2 = self.audio_buffer[:self.buffer_position]
            return np.concatenate([part1, part2])
    
    def clear_buffer(self) -> None:
        """
        [ПАМЯТЬ] - Очистить буфер
        """
        self.audio_buffer = np.zeros(self.buffer_size, dtype=np.float32)
        self.buffer_position = 0
        
        # Очищаем очередь
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except:
                break
        
        logger.debug("Аудио буфер очищен")
    
    def _get_audio_device(self) -> Optional[int]:
        """
        [ВЕДИ + ЧЕЛО] - Определить устройство аудио
        
        Returns:
            ID устройства или None (по умолчанию)
        """
        try:
            # Проверяем наличие устройств
            devices = sd.query_devices()
            if not devices:
                logger.warning("Аудиоустройства не найдены!")
                return None
            
            # Проверяем устройство по умолчанию
            try:
                default_device = sd.query_devices(kind='input')
                if default_device and default_device.get('max_input_channels', 0) > 0:
                    logger.debug(f"Устройство по умолчанию: {default_device['name']}")
                    return None  # Используем по умолчанию
                else:
                    logger.warning("Устройство ввода по умолчанию недоступно")
            except Exception as dev_err:
                logger.warning(f"Ошибка проверки устройства по умолчанию: {dev_err}")
                # Попробуем найти первое доступное устройство ввода
                for idx, device in enumerate(devices):
                    if device.get('max_input_channels', 0) > 0:
                        logger.info(f"Используем устройство [{idx}]: {device['name']}")
                        return idx
                return None
                
        except Exception as e:
            logger.warning(f"Ошибка проверки устройств: {e}")
            return None
        
        if self.source == "microphone":
            # Используем микрофон по умолчанию
            return None
        
        elif self.source == "system":
            # Попытка найти loopback устройство (для захвата системного аудио)
            devices = sd.query_devices()
            
            for idx, device in enumerate(devices):
                # Windows: ищем "Stereo Mix" или "What U Hear"
                # Linux: ищем "monitor"
                name = device['name'].lower()
                if any(keyword in name for keyword in ['stereo mix', 'what u hear', 'monitor', 'loopback']):
                    logger.info(f"Найдено loopback устройство: {device['name']}")
                    return idx
            
            logger.warning("Loopback устройство не найдено, используется микрофон по умолчанию")
            return None
        
        elif self.source == "both":
            # [ВЕДИ + ЧЕЛО] - Двойной режим: пробуем system, если не работает - microphone
            logger.info("[BOTH] Попытка захвата системного аудио...")
            
            # Сначала пробуем system
            devices = sd.query_devices()
            for idx, device in enumerate(devices):
                name = device['name'].lower()
                if any(keyword in name for keyword in ['stereo mix', 'what u hear', 'monitor', 'loopback']):
                    logger.info(f"[BOTH] Найдено loopback устройство: {device['name']}")
                    return idx
            
            # Если не нашли - используем микрофон
            logger.info("[BOTH] Loopback не найден, используется микрофон (захват только вашего голоса)")
            return None
        
        return None
    
    def set_callback(self, callback: Callable) -> None:
        """
        [ЧЕЛО + ИЖЕ] - Установить callback для обработки аудио
        
        Args:
            callback: Функция для вызова при получении аудио
        """
        self.audio_callback = callback
        logger.debug("Audio callback установлен")
    
    def list_devices(self) -> list:
        """
        [ВЕДИ] - Получить список доступных аудиоустройств
        
        Returns:
            Список устройств
        """
        try:
            devices = sd.query_devices()
            
            logger.info("Доступные аудиоустройства:")
            for idx, device in enumerate(devices):
                logger.info(f"  [{idx}] {device['name']} (in: {device['max_input_channels']}, out: {device['max_output_channels']})")
            
            # Показываем устройство по умолчанию
            default_input = sd.query_devices(kind='input')
            if default_input:
                logger.info(f"  [DEFAULT INPUT] {default_input['name']}")
            
            return devices
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка получения списка устройств: {e}")
            return []
    
    def is_running(self) -> bool:
        """
        Проверка, запущен ли захват
        
        Returns:
            True если захват активен
        """
        return self.is_recording.is_set()
    
    def __enter__(self):
        """Context manager support"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager support"""
        self.stop()
    
    def __del__(self):
        """Cleanup"""
        if self.is_recording.is_set():
            self.stop()

