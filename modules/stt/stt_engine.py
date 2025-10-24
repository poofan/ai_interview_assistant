"""
STT Engine - [МЫСЛЕТЕ + ВЕДИ]
Преобразование речи в текст через разные движки
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import Optional, Dict
from loguru import logger
import json
import wave
import io


class STTEngine(ABC):
    """
    Базовый класс для STT движков
    Архетипы:
    - МЫСЛЕТЕ: преобразование/распознавание
    - ВЕДИ: обработка аудио
    """
    
    @abstractmethod
    def transcribe(self, audio_data: np.ndarray, sample_rate: int = 16000) -> str:
        """
        Транскрибировать аудио в текст
        
        Args:
            audio_data: Аудиоданные (numpy array)
            sample_rate: Частота дискретизации
        
        Returns:
            Распознанный текст
        """
        pass
    
    @abstractmethod
    def is_ready(self) -> bool:
        """
        Проверка готовности движка
        
        Returns:
            True если движок готов
        """
        pass


class VoskSTT(STTEngine):
    """
    STT через Vosk (быстрый, оффлайн)
    Архетипы: [МЫСЛЕТЕ + ВЕДИ]
    """
    
    def __init__(self, model_path: str = "models/vosk-model-small-ru-0.22", language: str = "ru"):
        """
        Инициализация Vosk STT
        
        Args:
            model_path: Путь к модели Vosk
            language: Язык (ru, en, multi)
        """
        self.model_path = model_path
        self.language = language
        self.model = None
        self.recognizer = None
        
        # Thread-safe: используем Lock для потокобезопасности
        from threading import Lock
        self.lock = Lock()
        
        self._load_model()
    
    def _load_model(self) -> None:
        """
        [ВЕДИ + ДОБРО] - Загрузить модель Vosk
        """
        try:
            from vosk import Model, KaldiRecognizer
            
            logger.info(f"Загрузка Vosk модели: {self.model_path}")
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, 16000)
            
            logger.info("[OK] Vosk модель загружена")
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка загрузки Vosk модели: {e}")
            logger.warning("Убедитесь, что модель скачана в папку models/")
            raise
    
    def transcribe(self, audio_data: np.ndarray, sample_rate: int = 16000) -> str:
        """
        [МЫСЛЕТЕ + ВЕДИ] - Транскрибировать через Vosk
        
        Args:
            audio_data: Аудиоданные
            sample_rate: Частота дискретизации
        
        Returns:
            Распознанный текст
        """
        if not self.is_ready():
            logger.error("Vosk модель не готова")
            return ""
        
        # Thread-safe: блокируем доступ к recognizer
        with self.lock:
            try:
                from vosk import KaldiRecognizer
                
                # ИСПРАВЛЕНИЕ: Создаем НОВЫЙ recognizer для каждой транскрипции
                # Это решает проблему с queue_.empty() assertion
                recognizer = KaldiRecognizer(self.model, sample_rate)
                
                # Конвертируем в int16
                audio_int16 = (audio_data * 32767).astype(np.int16)
                audio_bytes = audio_int16.tobytes()
                
                # Распознаем
                if recognizer.AcceptWaveform(audio_bytes):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "")
                else:
                    result = json.loads(recognizer.PartialResult())
                    text = result.get("partial", "")
                
                # Финализируем
                recognizer.FinalResult()
                
                if text:
                    logger.debug(f"Vosk распознал: {text}")
                
                return text
            
            except Exception as e:
                logger.error(f"[ERROR] Ошибка распознавания Vosk: {e}")
                return ""
    
    def is_ready(self) -> bool:
        """Проверка готовности"""
        return self.model is not None and self.recognizer is not None


class WhisperSTT(STTEngine):
    """
    STT через OpenAI Whisper (точный, может быть медленным)
    Архетипы: [МЫСЛЕТЕ + ВЕДИ]
    """
    
    # [ШТОР] - Список галлюцинаций Whisper на тишине (фильтруем)
    HALLUCINATION_PATTERNS = [
        "субтитры",
        "спасибо за внимание",
        "спасибо что смотрите",
        "следующая серия",
        "продолжение следует",
        "н.новиков",
        "новикова",
        "amara.org",
        "subtitle",
        "thanks for watching"
    ]
    
    def __init__(self, model_size: str = "base", device: str = "cpu", language: str = "ru"):
        """
        Инициализация Whisper STT
        
        Args:
            model_size: Размер модели (tiny, base, small, medium, large)
            device: Устройство (cpu, cuda)
            language: Язык
        """
        self.model_size = model_size
        self.device = device
        self.language = language
        self.model = None
        
        # [НАВЬ] - Кэш последних результатов для детекции зацикливания
        self.last_results = []
        self.max_cache = 5
        
        self._load_model()
    
    def _load_model(self) -> None:
        """
        [ВЕДИ + ДОБРО] - Загрузить модель Whisper
        """
        try:
            import whisper
            
            logger.info(f"Загрузка Whisper модели: {self.model_size}")
            self.model = whisper.load_model(self.model_size, device=self.device)
            
            logger.info(f"[OK] Whisper модель загружена ({self.model_size}, {self.device})")
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка загрузки Whisper модели: {e}")
            raise
    
    def transcribe(self, audio_data: np.ndarray, sample_rate: int = 16000) -> str:
        """
        [МЫСЛЕТЕ + ВЕДИ] - Транскрибировать через Whisper
        
        Args:
            audio_data: Аудиоданные
            sample_rate: Частота дискретизации
        
        Returns:
            Распознанный текст
        """
        if not self.is_ready():
            logger.error("Whisper модель не готова")
            return ""
        
        try:
            # [ШТОР + НАВЬ] - Валидация и препроцессинг для GPU
            if len(audio_data) == 0:
                logger.warning("Пустой аудио буфер")
                return ""
            
            # Whisper ожидает float32 в диапазоне [-1, 1]
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Нормализуем если нужно
            max_val = np.max(np.abs(audio_data))
            if max_val > 1.0:
                audio_data = audio_data / max_val
            elif max_val < 0.001:  # Слишком тихо
                logger.debug("Аудио слишком тихое для распознавания")
                return ""
            
            # [CUDA FIX] Padding до минимальной длины для GPU стабильности
            min_length = sample_rate  # 1 секунда минимум
            if len(audio_data) < min_length:
                # Дополняем нулями до минимальной длины
                padding = np.zeros(min_length - len(audio_data), dtype=np.float32)
                audio_data = np.concatenate([audio_data, padding])
                logger.debug(f"Аудио дополнено до {len(audio_data)} сэмплов")
            
            # [CUDA FIX 2] Убеждаемся что длина кратна 16 (для CUDA оптимизации)
            remainder = len(audio_data) % 16
            if remainder != 0:
                pad_length = 16 - remainder
                padding = np.zeros(pad_length, dtype=np.float32)
                audio_data = np.concatenate([audio_data, padding])
                logger.debug(f"Выровнено до {len(audio_data)} сэмплов (кратно 16)")
            
            # Транскрибируем с защитой от GPU ошибок
            try:
                result = self.model.transcribe(
                    audio_data,
                    language=self.language,
                    fp16=False  # float32 для стабильности
                )
            except RuntimeError as cuda_err:
                # Если GPU ошибка - пробуем еще раз с принудительным CPU
                if "size" in str(cuda_err) or "CUDA" in str(cuda_err):
                    logger.warning(f"GPU ошибка в Whisper, переключаюсь на CPU: {cuda_err}")
                    import whisper
                    cpu_model = whisper.load_model(self.model_size, device="cpu")
                    result = cpu_model.transcribe(audio_data, language=self.language, fp16=False)
                else:
                    raise
            
            text = result.get("text", "").strip()
            
            if text:
                # [ШТОР + НАВЬ] - Фильтрация галлюцинаций
                if self._is_hallucination(text):
                    logger.debug(f"Отфильтрована галлюцинация Whisper: {text}")
                    return ""
                
                logger.debug(f"Whisper распознал: {text}")
            
            return text
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка распознавания Whisper: {e}")
            return ""
    
    def _is_hallucination(self, text: str) -> bool:
        """
        [ШТОР + МЫСЛЕТЕ] - Проверка на галлюцинацию Whisper
        
        Args:
            text: Распознанный текст
            
        Returns:
            True если это галлюцинация
        """
        text_lower = text.lower()
        
        # 1. Проверка на известные галлюцинационные паттерны
        for pattern in self.HALLUCINATION_PATTERNS:
            if pattern in text_lower:
                return True
        
        # 2. Проверка на повторение (зацикливание)
        self.last_results.append(text)
        if len(self.last_results) > self.max_cache:
            self.last_results.pop(0)
        
        # Если последние 3 результата одинаковые - это галлюцинация
        if len(self.last_results) >= 3:
            if self.last_results[-1] == self.last_results[-2] == self.last_results[-3]:
                return True
        
        # 3. Слишком короткий текст (<3 символов) - вероятно шум
        if len(text.strip()) < 3:
            return True
        
        return False
    
    def is_ready(self) -> bool:
        """Проверка готовности"""
        return self.model is not None


class FasterWhisperSTT(STTEngine):
    """
    STT через faster-whisper (оптимизирован для GPU, стабильнее)
    Архетипы: [МЫСЛЕТЕ + ВЕДИ + ЛАДЪ]
    """
    
    # [ШТОР] - Список галлюцинаций
    HALLUCINATION_PATTERNS = [
        "субтитры",
        "редактор",
        "корректор",
        "новиков",
        "закомолдина",
        "егоров",
        "спасибо за внимание",
        "спасибо что смотрите",
        "следующая серия",
        "продолжение следует",
        "amara.org",
        "subtitle",
        "thanks for watching"
    ]
    
    def __init__(self, model_size: str = "base", device: str = "cpu", language: str = "ru"):
        """
        Инициализация faster-whisper STT
        
        Args:
            model_size: Размер модели (tiny, base, small, medium, large)
            device: Устройство (cpu, cuda)
            language: Язык
        """
        self.model_size = model_size
        self.device = device
        self.language = language
        self.model = None
        
        # [НАВЬ] - Кэш последних результатов
        self.last_results = []
        self.max_cache = 5
        
        self._load_model()
    
    def _load_model(self) -> None:
        """
        [ВЕДИ + ДОБРО] - Загрузить модель faster-whisper
        """
        try:
            from faster_whisper import WhisperModel
            
            logger.info(f"Загрузка faster-whisper модели: {self.model_size}")
            
            # faster-whisper использует разные значения для device
            device_name = "cuda" if self.device == "cuda" else "cpu"
            # int8 для GTX 1060 (Pascal) - быстро и стабильно
            compute_type = "int8"
            
            self.model = WhisperModel(
                self.model_size,
                device=device_name,
                compute_type=compute_type
            )
            
            logger.info(f"[OK] faster-whisper модель загружена ({self.model_size}, {device_name}, {compute_type})")
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка загрузки faster-whisper: {e}")
            raise
    
    def transcribe(self, audio_data: np.ndarray, sample_rate: int = 16000) -> str:
        """
        [МЫСЛЕТЕ + ВЕДИ] - Транскрибировать через faster-whisper
        
        Args:
            audio_data: Аудиоданные
            sample_rate: Частота дискретизации
        
        Returns:
            Распознанный текст
        """
        if not self.is_ready():
            logger.error("faster-whisper модель не готова")
            return ""
        
        try:
            # [ШТОР] - Валидация
            if len(audio_data) == 0:
                logger.debug("Пустой аудио буфер")
                return ""
            
            # Проверка громкости
            max_val = np.max(np.abs(audio_data))
            if max_val < 0.001:
                logger.debug("Аудио слишком тихое для распознавания")
                return ""
            
            # Нормализация
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            if max_val > 1.0:
                audio_data = audio_data / max_val
            
            # faster-whisper транскрипция
            segments, info = self.model.transcribe(
                audio_data,
                language=self.language,
                beam_size=5,
                vad_filter=False  # Отключен - используем свой фильтр галлюцинаций
            )
            
            # Собираем текст из сегментов
            text_parts = []
            for segment in segments:
                text_parts.append(segment.text)
            
            text = " ".join(text_parts).strip()
            
            if text:
                # [ШТОР] - Фильтрация галлюцинаций
                if self._is_hallucination(text):
                    logger.debug(f"Отфильтрована галлюцинация: {text}")
                    return ""
                
                logger.debug(f"faster-whisper распознал: {text}")
            
            return text
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка распознавания faster-whisper: {e}")
            return ""
    
    def _is_hallucination(self, text: str) -> bool:
        """[ШТОР] - Проверка на галлюцинацию"""
        text_lower = text.lower()
        
        for pattern in self.HALLUCINATION_PATTERNS:
            if pattern in text_lower:
                return True
        
        self.last_results.append(text)
        if len(self.last_results) > self.max_cache:
            self.last_results.pop(0)
        
        if len(self.last_results) >= 3:
            if self.last_results[-1] == self.last_results[-2] == self.last_results[-3]:
                return True
        
        if len(text.strip()) < 3:
            return True
        
        return False
    
    def is_ready(self) -> bool:
        """Проверка готовности"""
        return self.model is not None


class STTManager:
    """
    Менеджер для управления разными STT движками
    Архетипы: [ДОБРО + МЫСЛЕТЕ]
    """
    
    def __init__(self, default_engine: str = "vosk", config: Optional[Dict] = None):
        """
        Инициализация менеджера STT
        
        Args:
            default_engine: Движок по умолчанию (vosk, whisper)
            config: Конфигурация движков
        """
        self.config = config or {}
        self.engines: Dict[str, STTEngine] = {}
        self.current_engine = default_engine
        
        self._init_engines()
    
    def _init_engines(self) -> None:
        """
        [ДОБРО + ВЕДИ] - Инициализировать доступные движки
        """
        # Попытка инициализации Vosk
        try:
            vosk_config = self.config.get("vosk", {})
            model_path = vosk_config.get("model_path", "models/vosk-model-small-ru-0.22")
            language = self.config.get("language", "ru")
            
            self.engines["vosk"] = VoskSTT(model_path=model_path, language=language)
            logger.info("[OK] Vosk STT доступен")
        
        except Exception as e:
            logger.warning(f"Vosk STT недоступен: {e}")
        
        # Попытка инициализации Whisper (используем faster-whisper для GPU стабильности)
        try:
            whisper_config = self.config.get("whisper", {})
            model_size = whisper_config.get("model_size", "base")
            device = whisper_config.get("device", "cpu")
            language = self.config.get("language", "ru")
            
            # Используем faster-whisper - стабильнее на CUDA
            self.engines["whisper"] = FasterWhisperSTT(
                model_size=model_size,
                device=device,
                language=language
            )
            logger.info("[OK] Whisper STT доступен (faster-whisper)")
        
        except Exception as e:
            logger.warning(f"Whisper STT недоступен: {e}")
        
        if not self.engines:
            raise RuntimeError("Ни один STT движок не доступен!")
    
    def transcribe(self, audio_data: np.ndarray, sample_rate: int = 16000, engine: Optional[str] = None) -> str:
        """
        [МЫСЛЕТЕ] - Транскрибировать аудио
        
        Args:
            audio_data: Аудиоданные
            sample_rate: Частота
            engine: Движок (None = используется текущий)
        
        Returns:
            Распознанный текст
        """
        engine_name = engine or self.current_engine
        
        if engine_name not in self.engines:
            logger.error(f"Движок {engine_name} недоступен")
            # Fallback на любой доступный
            engine_name = list(self.engines.keys())[0]
            logger.info(f"Используется fallback движок: {engine_name}")
        
        stt_engine = self.engines[engine_name]
        return stt_engine.transcribe(audio_data, sample_rate)
    
    def switch_engine(self, engine_name: str) -> bool:
        """
        [ДОБРО] - Переключить движок
        
        Args:
            engine_name: Имя движка (vosk, whisper)
        
        Returns:
            True если успешно
        """
        if engine_name not in self.engines:
            logger.error(f"Движок {engine_name} недоступен")
            return False
        
        old_engine = self.current_engine
        self.current_engine = engine_name
        logger.info(f"Движок переключен: {old_engine} -> {engine_name}")
        return True
    
    def get_available_engines(self) -> list:
        """
        [ВЕДИ] - Получить список доступных движков
        
        Returns:
            Список имен движков
        """
        return list(self.engines.keys())
    
    def get_current_engine(self) -> str:
        """
        Получить текущий движок
        
        Returns:
            Имя текущего движка
        """
        return self.current_engine


