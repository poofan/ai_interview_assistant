"""
Question Detector - [ЧЕЛО + МЫСЛЕТЕ]
Определение вопросительных конструкций в тексте
"""

import re
from typing import List, Optional, Tuple
from loguru import logger


class QuestionDetector:
    """
    Детектор вопросов
    Архетипы:
    - ЧЕЛО: распознавание паттернов
    - МЫСЛЕТЕ: анализ текста
    - ЖИВЕТЕ: триггер действия
    """
    
    def __init__(
        self,
        mode: str = "hybrid",
        confidence_threshold: float = 0.7,
        patterns: Optional[List[str]] = None
    ):
        """
        Инициализация детектора вопросов
        
        Args:
            mode: Режим работы (auto, manual, hybrid, regex, ml)
            confidence_threshold: Порог уверенности для ML
            patterns: Regex паттерны для определения вопросов
        """
        self.mode = mode
        self.confidence_threshold = confidence_threshold
        
        # Стандартные паттерны
        self.patterns = patterns or [
            r'\?$',  # Заканчивается на ?
            r'^как\s',  # Начинается с "как"
            r'^что\s',  # "что"
            r'^почему\s',  # "почему"
            r'^зачем\s',  # "зачем"
            r'^где\s',  # "где"
            r'^когда\s',  # "когда"
            r'^кто\s',  # "кто"
            r'^какой\s',  # "какой"
            r'^какая\s',  # "какая"
            r'^какие\s',  # "какие"
            r'^можешь?\s',  # "можешь", "можете"
            r'^расскажи',  # "расскажи"
            r'^объясни',  # "объясни"
            r'^опиши',  # "опиши"
            r'^в чем\s',  # "в чем"
            r'^чем отличается',  # "чем отличается"
            # English patterns
            r'^what\s',
            r'^how\s',
            r'^why\s',
            r'^when\s',
            r'^where\s',
            r'^who\s',
            r'^which\s',
            r'^can you\s',
            r'^could you\s',
            r'^explain\s',
            r'^describe\s',
        ]
        
        # Компилируем паттерны
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.patterns]
        
        # ML модель (опционально)
        self.ml_model = None
        self.ml_tokenizer = None
        
        if self.mode in ["ml", "hybrid"]:
            self._init_ml_model()
        
        logger.info(f"[OK] QuestionDetector инициализирован (режим: {mode})")
    
    def _init_ml_model(self) -> None:
        """
        [МЫСЛЕТЕ + ВЕДИ] - Инициализировать ML модель для детекции
        """
        try:
            # Проверяем совместимость NumPy
            import numpy as np
            numpy_version = tuple(map(int, np.__version__.split('.')[:2]))
            
            if numpy_version[0] >= 2:
                logger.warning(f"NumPy {np.__version__} несовместим с transformers, отключаем ML детекцию")
                raise ImportError("NumPy 2.x несовместим с TensorFlow/transformers")
            
            from transformers import pipeline
            
            logger.info("Загрузка ML модели для детекции вопросов...")
            
            # Используем zero-shot classification
            self.ml_model = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",  # или multilingual модель
                device=-1  # CPU
            )
            
            logger.info("[OK] ML модель загружена")
        
        except Exception as e:
            logger.warning(f"ML модель недоступна, используется regex детекция")
            logger.debug(f"Причина: {str(e)[:100]}")
            
            if self.mode == "ml":
                self.mode = "regex"
                logger.info("Режим изменен с 'ml' на 'regex'")
    
    def is_question(self, text: str) -> Tuple[bool, float]:
        """
        [ЧЕЛО + МЫСЛЕТЕ] - Определить, является ли текст вопросом
        
        Args:
            text: Текст для анализа
        
        Returns:
            (is_question, confidence)
        """
        if not text or not text.strip():
            return False, 0.0
        
        text = text.strip()
        
        # Режим auto (manual) - не используем автодетекцию
        if self.mode == "manual":
            return False, 0.0
        
        # Regex детекция
        if self.mode in ["auto", "regex", "hybrid"]:
            is_q_regex, conf_regex = self._regex_detect(text)
            
            if self.mode == "regex":
                return is_q_regex, conf_regex
            
            # Для hybrid продолжаем с ML
            if self.mode == "auto":
                return is_q_regex, conf_regex
        
        # ML детекция
        if self.mode in ["ml", "hybrid"] and self.ml_model:
            is_q_ml, conf_ml = self._ml_detect(text)
            
            if self.mode == "ml":
                return is_q_ml, conf_ml
            
            # Hybrid: комбинируем результаты
            if is_q_regex and conf_regex > 0.8:
                return True, conf_regex
            elif is_q_ml:
                return True, conf_ml
            else:
                return False, max(conf_regex, conf_ml)
        
        # Fallback
        return self._regex_detect(text)
    
    def _regex_detect(self, text: str) -> Tuple[bool, float]:
        """
        [ЧЕЛО] - Детекция через регулярные выражения
        
        Args:
            text: Текст для анализа
        
        Returns:
            (is_question, confidence)
        """
        # Проверяем каждый паттерн
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                logger.debug(f"Regex обнаружил вопрос: {text[:50]}...")
                return True, 0.9
        
        # Дополнительная проверка: содержит вопросительные слова
        question_words_ru = ['как', 'что', 'почему', 'зачем', 'где', 'когда', 'кто', 'какой']
        question_words_en = ['what', 'how', 'why', 'when', 'where', 'who', 'which']
        
        text_lower = text.lower()
        words = text_lower.split()
        
        for qword in question_words_ru + question_words_en:
            if qword in words:
                logger.debug(f"Обнаружено вопросительное слово '{qword}': {text[:50]}...")
                return True, 0.7
        
        return False, 0.0
    
    def _ml_detect(self, text: str) -> Tuple[bool, float]:
        """
        [МЫСЛЕТЕ] - ML детекция вопросов
        
        Args:
            text: Текст для анализа
        
        Returns:
            (is_question, confidence)
        """
        if not self.ml_model:
            return False, 0.0
        
        try:
            result = self.ml_model(
                text,
                candidate_labels=["question", "statement"],
                hypothesis_template="This is a {}."
            )
            
            # Берем лучший результат
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            
            is_question = top_label == "question" and top_score >= self.confidence_threshold
            
            if is_question:
                logger.debug(f"ML обнаружил вопрос (conf: {top_score:.2f}): {text[:50]}...")
            
            return is_question, top_score if is_question else 0.0
        
        except Exception as e:
            logger.error(f"Ошибка ML детекции: {e}")
            return False, 0.0
    
    def should_trigger(self, text: str) -> bool:
        """
        [ЖИВЕТЕ + ЧЕЛО] - Должен ли сработать триггер генерации ответа
        
        Args:
            text: Текст для проверки
        
        Returns:
            True если нужно генерировать ответ
        """
        is_q, confidence = self.is_question(text)
        
        if is_q:
            logger.info(f"[TRIGGER] Триггер вопроса! (confidence: {confidence:.2f})")
            return True
        
        return False
    
    def analyze_text(self, text: str) -> dict:
        """
        [МЫСЛЕТЕ] - Полный анализ текста
        
        Args:
            text: Текст для анализа
        
        Returns:
            Словарь с результатами анализа
        """
        is_q, confidence = self.is_question(text)
        
        # Проверяем отдельно regex и ML
        is_q_regex, conf_regex = self._regex_detect(text)
        
        is_q_ml, conf_ml = False, 0.0
        if self.ml_model and self.mode in ["ml", "hybrid"]:
            is_q_ml, conf_ml = self._ml_detect(text)
        
        return {
            "text": text,
            "is_question": is_q,
            "confidence": confidence,
            "regex_detection": {
                "is_question": is_q_regex,
                "confidence": conf_regex
            },
            "ml_detection": {
                "is_question": is_q_ml,
                "confidence": conf_ml,
                "available": self.ml_model is not None
            },
            "should_trigger": is_q
        }
    
    def set_mode(self, mode: str) -> None:
        """
        [ДОБРО] - Изменить режим работы
        
        Args:
            mode: Новый режим (auto, manual, hybrid, regex, ml)
        """
        old_mode = self.mode
        self.mode = mode
        logger.info(f"Режим детекции изменен: {old_mode} -> {mode}")
    
    def add_pattern(self, pattern: str) -> None:
        """
        [ДОБРО] - Добавить новый regex паттерн
        
        Args:
            pattern: Regex паттерн
        """
        self.patterns.append(pattern)
        self.compiled_patterns.append(re.compile(pattern, re.IGNORECASE))
        logger.debug(f"Добавлен паттерн: {pattern}")

