"""
Prompt Manager - [СЛОВО + ДОБРО]
Управление шаблонами промптов для разных типов собеседований
"""

from typing import Dict, Optional
from enum import Enum
from loguru import logger
import re


class InterviewProfile(Enum):
    """Типы собеседований"""
    ALGORITHMS = "algorithms"        # Алгоритмические задачи
    FRONTEND = "frontend"            # Frontend разработка
    BACKEND = "backend"              # Backend разработка
    SYSTEM_DESIGN = "system_design"  # System design
    THEORY = "theory"                # Теоретические вопросы
    CODE_REVIEW = "code_review"      # Ревью кода
    GENERAL = "general"              # Общие вопросы


class PromptManager:
    """
    Менеджер промптов
    Архетипы:
    - СЛОВО: шаблоны текста
    - ДОБРО: организация и выбор
    - ЧЕЛО: определение контекста
    """
    
    # Шаблоны системных промптов (с переменными)
    SYSTEM_PROMPT_TEMPLATES = {
        InterviewProfile.ALGORITHMS: """Ты - эксперт по алгоритмам и структурам данных. 

ВАЖНО: Когда получаешь алгоритмическую задачу:
1. Дай ГОТОВОЕ РАБОЧЕЕ РЕШЕНИЕ с кодом на {language}
2. Добавь комментарии к коду
3. Укажи сложность O(n)
4. Кратко объясни подход (1-2 предложения)

Формат ответа - рабочий код с комментариями, сложность и краткое объяснение.""",

        InterviewProfile.FRONTEND: """Ты - эксперт по Frontend разработке (React, JavaScript, TypeScript, CSS).

ВАЖНО: При вопросах о коде:
1. Дай ГОТОВОЕ РЕШЕНИЕ с кодом на {language}
2. Используй современные практики
3. Добавь примеры использования

При теоретических вопросах - отвечай кратко с примерами.""",

        InterviewProfile.BACKEND: """Ты - эксперт по Backend разработке ({language}, базы данных, API).

ВАЖНО: При задачах:
1. Дай ГОТОВОЕ РЕШЕНИЕ с кодом на {language}
2. Учитывай масштабируемость и безопасность
3. Добавь примеры SQL/API endpoints если нужно

Отвечай практично с акцентом на production-ready код.""",

        InterviewProfile.SYSTEM_DESIGN: """Ты - архитектор систем, эксперт по system design.

Формат ответа:
1. Компоненты системы
2. Схема взаимодействия
3. Технологии (конкретные названия)
4. Узкие места и решения

Будь конкретен, избегай общих фраз.""",

        InterviewProfile.CODE_REVIEW: """Ты - senior разработчик, делаешь code review.

При получении кода:
1. Укажи проблемы (если есть)
2. Предложи УЛУЧШЕННУЮ версию кода
3. Объясни почему так лучше

Будь конструктивен и конкретен.""",

        InterviewProfile.THEORY: """Ты - технический консультант.

Отвечай на теоретические вопросы:
- Кратко и по делу
- С примерами где уместно
- Структурированно

Избегай воды и общих фраз.""",

        InterviewProfile.GENERAL: """Ты - профессиональный технический консультант.

Давай краткие, точные и практичные ответы на вопросы собеседований.
Используй примеры кода когда уместно."""
    }
    
    # Ключевые слова для определения типа вопроса (порядок важен - сверху приоритетнее!)
    QUESTION_PATTERNS = {
        # THEORY - должен быть ПЕРВЫМ (высший приоритет для теоретических вопросов)
        InterviewProfile.THEORY: [
            r'^что\s+такое',
            r'^дайте.*характеристик',
            r'^объясните',
            r'^опишите',
            r'^зачем',
            r'^почему.*нужн',
            r'^в\s+чем\s+(разница|отличие)',
            r'^каки[ем]\s+(принцип|свойств)',
            r'immutable',
            r'полиморфизм',
            r'инкапсуляци',
            r'наследовани',
            r'принцип.*ооп',
            r'паттерн.*проектирования',
            r'solid',
        ],
        
        InterviewProfile.ALGORITHMS: [
            r'напиш[иь].*функци[юя]',
            r'реализу[йи]',  # Без "функци" - любое "реализуй"
            r'implement',    # Любое implement
            r'write.*function',
            r'код.*для',
            r'решение.*задач',
            r'решить.*задач',
            r'leetcode',
            r'binary search|бинарн',
            r'sorting|сортиро|quicksort|mergesort',
            r'дерев[оа]',
            r'граф',
            r'динамическ.*программ',
            r'рекурси',
            r'массив',
            r'linked list|связн.*список',
            r'hash.*table|хеш',
            r'stack|queue|очеред|стек',
            r'find.*element|найти.*элемент',
        ],
        
        InterviewProfile.FRONTEND: [
            r'react',
            r'component',
            r'hook',
            r'state',
            r'redux',
            r'css',
            r'html',
            r'dom',
            r'event',
            r'render',
        ],
        
        InterviewProfile.BACKEND: [
            r'api',
            r'database',
            r'sql',
            r'rest',
            r'endpoint',
            r'сервер',
            r'middleware',
            r'authentication',
            r'postgres|mysql|mongo',
        ],
        
        InterviewProfile.SYSTEM_DESIGN: [
            r'спроектир',
            r'design.*system',
            r'архитектур',
            r'масштаб',
            r'микросервис',
            r'load.*balanc',
            r'кэш',
            r'sharding',
        ],
        
        InterviewProfile.CODE_REVIEW: [
            r'что.*не.*так',
            r'ошибк.*в.*код',
            r'исправ.*код',
            r'улучш.*код',
            r'review',
            r'рефактор',
        ],
    }
    
    # Паттерны для автоопределения языка программирования
    LANGUAGE_PATTERNS = {
        'Java': [r'\bJava\b', r'\bclass\s+\w+', r'public\s+static', r'System\.out'],
        'C++': [r'\bC\+\+\b', r'\bstd::', r'#include', r'iostream'],
        'JavaScript': [r'\bJavaScript\b', r'\bJS\b', r'const\s+', r'let\s+', r'=>', r'npm'],
        'TypeScript': [r'\bTypeScript\b', r'\bTS\b', r'interface\s+', r'type\s+\w+\s*='],
        'Go': [r'\bGolang\b', r'\bGo\b', r'func\s+', r'package\s+main'],
        'C#': [r'\bC#\b', r'\.NET', r'using\s+System'],
        'Rust': [r'\bRust\b', r'fn\s+', r'let\s+mut'],
        'Python': [r'\bPython\b', r'def\s+', r'import\s+', r'print\('],
    }
    
    def __init__(
        self, 
        default_profile: InterviewProfile = InterviewProfile.ALGORITHMS,
        programming_language: str = "Python",
        auto_detect_language: bool = True
    ):
        """
        Инициализация менеджера промптов
        
        Args:
            default_profile: Профиль по умолчанию
            programming_language: Язык программирования по умолчанию
            auto_detect_language: Автоопределение языка из вопроса
        """
        self.current_profile = default_profile
        self.programming_language = programming_language
        self.auto_detect_language = auto_detect_language
        self.custom_prompts: Dict[str, str] = {}
        
        logger.info(f"[OK] PromptManager инициализирован (профиль: {default_profile.value}, язык: {programming_language})")
    
    def get_system_prompt(self, profile: Optional[InterviewProfile] = None, language: Optional[str] = None) -> str:
        """
        [СЛОВО + ВЕДИ] - Получить системный промпт
        
        Args:
            profile: Профиль (None = текущий)
            language: Язык программирования (None = текущий)
        
        Returns:
            Системный промпт
        """
        profile = profile or self.current_profile
        language = language or self.programming_language
        
        # Проверяем кастомный промпт
        if profile.value in self.custom_prompts:
            template = self.custom_prompts[profile.value]
        else:
            template = self.SYSTEM_PROMPT_TEMPLATES.get(
                profile, 
                self.SYSTEM_PROMPT_TEMPLATES[InterviewProfile.GENERAL]
            )
        
        # Подставляем язык
        return template.replace("{language}", language)
    
    def detect_question_type(self, question: str) -> InterviewProfile:
        """
        [ЧЕЛО + МЫСЛЕТЕ] - Определить тип вопроса
        
        Args:
            question: Текст вопроса
        
        Returns:
            Определенный профиль
        """
        question_lower = question.lower()
        
        # ВАЖНО: Проверяем в порядке приоритета!
        # THEORY должен проверяться ПЕРВЫМ
        
        # 1. Сначала проверяем THEORY (высший приоритет)
        if InterviewProfile.THEORY in self.QUESTION_PATTERNS:
            for pattern in self.QUESTION_PATTERNS[InterviewProfile.THEORY]:
                if re.search(pattern, question_lower, re.IGNORECASE):
                    logger.info(f"[INFO] Определен тип: THEORY (паттерн: {pattern})")
                    return InterviewProfile.THEORY
        
        # 2. Затем остальные типы по score
        scores = {}
        
        for profile, patterns in self.QUESTION_PATTERNS.items():
            if profile == InterviewProfile.THEORY:
                continue  # Уже проверили выше
            
            score = 0
            matched_patterns = []
            for pattern in patterns:
                if re.search(pattern, question_lower, re.IGNORECASE):
                    score += 1
                    matched_patterns.append(pattern)
            
            if score > 0:
                scores[profile] = (score, matched_patterns)
        
        # Находим профиль с максимальным score
        if scores:
            best_profile = max(scores.items(), key=lambda x: x[1][0])
            if best_profile[1][0] > 0:
                logger.info(f"[INFO] Определен тип: {best_profile[0].value} (score: {best_profile[1][0]}, паттерны: {best_profile[1][1][:2]})")
                return best_profile[0]
        
        # Fallback - возвращаем THEORY для общих вопросов
        logger.debug(f"Тип не определен, используется THEORY")
        return InterviewProfile.THEORY
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        [ЧЕЛО + МЫСЛЕТЕ] - Автоопределение языка программирования из текста
        
        Args:
            text: Текст вопроса
        
        Returns:
            Определенный язык или None
        """
        if not self.auto_detect_language:
            return None
        
        text_lower = text.lower()
        scores = {}
        
        for language, patterns in self.LANGUAGE_PATTERNS.items():
            score = sum(1 for pattern in patterns if re.search(pattern, text, re.IGNORECASE))
            if score > 0:
                scores[language] = score
        
        if scores:
            detected = max(scores.items(), key=lambda x: x[1])
            if detected[1] >= 2:  # Минимум 2 совпадения для уверенности
                logger.debug(f"Автоопределен язык: {detected[0]}")
                return detected[0]
        
        return None
    
    def enhance_question(self, question: str, profile: Optional[InterviewProfile] = None) -> str:
        """
        [МЫСЛЕТЕ + СЛОВО] - Улучшить вопрос добавлением инструкций
        
        Args:
            question: Исходный вопрос
            profile: Профиль (автоопределение если None)
        
        Returns:
            Улучшенный вопрос
        """
        # Автоопределение типа
        if profile is None:
            profile = self.detect_question_type(question)
        
        # Автоопределение языка из вопроса
        detected_language = self.detect_language(question)
        language = detected_language or self.programming_language
        
        if detected_language and detected_language != self.programming_language:
            logger.info(f"[INFO] Определен язык в вопросе: {detected_language}")
        
        # Добавляем инструкции в зависимости от типа
        if profile == InterviewProfile.THEORY:
            # Для THEORY - НЕ НУЖЕН КОД, только объяснение
            enhanced = f"""{question}

ВАЖНО: Это теоретический вопрос. Дай КРАТКОЕ ОБЪЯСНЕНИЕ (2-4 предложения) с примером если уместно. 
НЕ ПИШИ КОД, только текстовое объяснение концепции."""
            
        elif profile == InterviewProfile.ALGORITHMS:
            enhanced = f"""{question}

ВАЖНО: Дай ГОТОВОЕ РЕШЕНИЕ с кодом на {language}. Включи:
- Рабочий код с комментариями
- Сложность O(n)
- Краткое объяснение подхода"""
            
        elif profile == InterviewProfile.CODE_REVIEW:
            enhanced = f"""{question}

Проанализируй код и дай ИСПРАВЛЕННУЮ версию на {language} с объяснением что изменено."""
            
        elif profile in [InterviewProfile.FRONTEND, InterviewProfile.BACKEND]:
            enhanced = f"""{question}

Дай ГОТОВОЕ РЕШЕНИЕ с кодом на {language} и кратким объяснением."""
        
        elif profile == InterviewProfile.SYSTEM_DESIGN:
            enhanced = f"""{question}

Дай схему системы с компонентами, технологиями и решениями узких мест."""
            
        else:
            enhanced = question
        
        return enhanced
    
    def set_profile(self, profile: InterviewProfile) -> None:
        """
        [ДОБРО] - Установить текущий профиль
        
        Args:
            profile: Новый профиль
        """
        old_profile = self.current_profile
        self.current_profile = profile
        logger.info(f"Профиль изменен: {old_profile.value} -> {profile.value}")
    
    def set_custom_prompt(self, profile: InterviewProfile, prompt: str) -> None:
        """
        [ДОБРО + СЛОВО] - Установить кастомный промпт
        
        Args:
            profile: Профиль
            prompt: Кастомный промпт
        """
        self.custom_prompts[profile.value] = prompt
        logger.info(f"Установлен кастомный промпт для {profile.value}")
    
    def set_programming_language(self, language: str) -> None:
        """
        [ДОБРО] - Установить язык программирования
        
        Args:
            language: Язык (Python, Java, C++, etc.)
        """
        old_lang = self.programming_language
        self.programming_language = language
        logger.info(f"Язык программирования изменен: {old_lang} -> {language}")
    
    def get_profile_list(self) -> list:
        """
        [ВЕДИ] - Получить список доступных профилей
        
        Returns:
            Список профилей
        """
        return [p.value for p in InterviewProfile]
    
    def get_supported_languages(self) -> list:
        """
        [ВЕДИ] - Получить список поддерживаемых языков
        
        Returns:
            Список языков
        """
        return list(self.LANGUAGE_PATTERNS.keys())

