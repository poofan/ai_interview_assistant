"""
Context Manager - [ПАМЯТЬ + ДОБРО]
Управление историей диалога и контекстом
"""

import json
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
from loguru import logger


class ContextManager:
    """
    Менеджер контекста диалога
    Архетипы:
    - ПАМЯТЬ: хранение истории
    - ДОБРО: организация сообщений
    - СЛОВО: запись диалога
    """
    
    def __init__(
        self,
        max_messages: int = 20,
        max_tokens: int = 4000,
        save_history: bool = True,
        history_path: str = "data/sessions"
    ):
        """
        Инициализация менеджера контекста
        
        Args:
            max_messages: Максимальное количество сообщений в контексте
            max_tokens: Примерный максимум токенов
            save_history: Сохранять ли историю на диск
            history_path: Путь для сохранения истории
        """
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.save_history = save_history
        self.history_path = Path(history_path)
        
        # История диалога
        self.messages: List[Dict[str, str]] = []
        
        # Метаданные сессии
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_start = datetime.now()
        
        # Создаем директорию если нужно
        if self.save_history:
            self.history_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"[OK] ContextManager инициализирован (session: {self.session_id})")
    
    def add_message(self, role: str, content: str) -> None:
        """
        [ПАМЯТЬ + ДОБРО] - Добавить сообщение в контекст
        
        Args:
            role: Роль (user, assistant, system)
            content: Содержимое сообщения
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.messages.append(message)
        logger.debug(f"Добавлено сообщение ({role}): {content[:50]}...")
        
        # Автоматическая обрезка если слишком много сообщений или токенов
        if len(self.messages) > self.max_messages:
            self._trim_context()
        
        # Проверка токенов
        estimated_tokens = self.estimate_tokens()
        if estimated_tokens > self.max_tokens:
            logger.warning(f"Превышен лимит токенов ({estimated_tokens}/{self.max_tokens}), обрезаем контекст")
            self._trim_context()
    
    def add_user_message(self, content: str) -> None:
        """
        [ПАМЯТЬ] - Добавить сообщение пользователя
        
        Args:
            content: Вопрос/сообщение пользователя
        """
        self.add_message("user", content)
    
    def add_assistant_message(self, content: str) -> None:
        """
        [ПАМЯТЬ] - Добавить ответ ассистента
        
        Args:
            content: Ответ ассистента
        """
        self.add_message("assistant", content)
    
    def get_context(self, include_timestamps: bool = False) -> List[Dict[str, str]]:
        """
        [ВЕДИ + ПАМЯТЬ] - Получить контекст для отправки в LLM
        
        Args:
            include_timestamps: Включать ли метки времени
        
        Returns:
            Список сообщений для LLM
        """
        if include_timestamps:
            return self.messages.copy()
        
        # Убираем timestamps для LLM
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.messages
        ]
    
    def get_recent_context(self, n_messages: int = 5) -> List[Dict[str, str]]:
        """
        [ПАМЯТЬ] - Получить последние N сообщений
        
        Args:
            n_messages: Количество последних сообщений
        
        Returns:
            Последние сообщения
        """
        recent = self.messages[-n_messages:] if len(self.messages) > n_messages else self.messages
        
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in recent
        ]
    
    def _trim_context(self) -> None:
        """
        [ДОБРО + ПАМЯТЬ] - Обрезать контекст до нужного размера
        Удаляет старые сообщения, оставляя самые свежие
        """
        if len(self.messages) <= self.max_messages:
            return
        
        # Удаляем старые сообщения, сохраняя последние
        removed = len(self.messages) - self.max_messages
        self.messages = self.messages[-self.max_messages:]
        
        logger.debug(f"Контекст обрезан: удалено {removed} старых сообщений")
    
    def clear_context(self) -> None:
        """
        [ПАМЯТЬ] - Очистить контекст (начать новую беседу)
        """
        old_count = len(self.messages)
        self.messages = []
        logger.info(f"Контекст очищен (было {old_count} сообщений)")
    
    def save_session(self, filename: Optional[str] = None) -> str:
        """
        [ПАМЯТЬ + СЛОВО] - Сохранить сессию на диск
        
        Args:
            filename: Имя файла (опционально)
        
        Returns:
            Путь к сохраненному файлу
        """
        if not self.save_history:
            logger.warning("Сохранение истории отключено в настройках")
            return ""
        
        if not filename:
            filename = f"session_{self.session_id}.json"
        
        filepath = self.history_path / filename
        
        session_data = {
            "session_id": self.session_id,
            "session_start": self.session_start.isoformat(),
            "session_end": datetime.now().isoformat(),
            "message_count": len(self.messages),
            "messages": self.messages
        }
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"[OK] Сессия сохранена: {filepath}")
            return str(filepath)
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка сохранения сессии: {e}")
            raise
    
    def load_session(self, filepath: str) -> bool:
        """
        [ПАМЯТЬ + ВЕДИ] - Загрузить сессию с диска
        
        Args:
            filepath: Путь к файлу сессии
        
        Returns:
            True если загрузка успешна
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            
            self.messages = session_data.get("messages", [])
            self.session_id = session_data.get("session_id", self.session_id)
            
            logger.info(f"[OK] Сессия загружена: {filepath} ({len(self.messages)} сообщений)")
            return True
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка загрузки сессии: {e}")
            return False
    
    def export_to_markdown(self, filename: Optional[str] = None) -> str:
        """
        [СЛОВО + ЛИЧЬ] - Экспортировать в Markdown
        
        Args:
            filename: Имя файла (опционально)
        
        Returns:
            Путь к экспортированному файлу
        """
        if not filename:
            filename = f"session_{self.session_id}.md"
        
        filepath = self.history_path / filename
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# Interview Session {self.session_id}\n\n")
                f.write(f"**Start:** {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"**Messages:** {len(self.messages)}\n\n")
                f.write("---\n\n")
                
                for msg in self.messages:
                    role_emoji = "🙋" if msg["role"] == "user" else "🤖"
                    role_label = "Question" if msg["role"] == "user" else "Answer"
                    timestamp = msg.get("timestamp", "")
                    
                    f.write(f"## {role_emoji} {role_label}\n")
                    if timestamp:
                        f.write(f"*{timestamp}*\n\n")
                    f.write(f"{msg['content']}\n\n")
                    f.write("---\n\n")
            
            logger.info(f"[OK] Сессия экспортирована в Markdown: {filepath}")
            return str(filepath)
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка экспорта в Markdown: {e}")
            raise
    
    def estimate_tokens(self) -> int:
        """
        [МЫСЛЕТЕ] - Примерная оценка количества токенов
        
        Returns:
            Примерное количество токенов в контексте
        """
        # Простая эвристика: ~3 символа = 1 токен для русского/английского
        total_chars = sum(len(msg["content"]) for msg in self.messages)
        return total_chars // 3
    
    def get_statistics(self) -> Dict[str, any]:
        """
        [ВЕДИ + МЫСЛЕТЕ] - Получить статистику сессии
        
        Returns:
            Словарь со статистикой
        """
        user_messages = [m for m in self.messages if m["role"] == "user"]
        assistant_messages = [m for m in self.messages if m["role"] == "assistant"]
        
        return {
            "session_id": self.session_id,
            "duration_minutes": (datetime.now() - self.session_start).total_seconds() / 60,
            "total_messages": len(self.messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "avg_question_length": sum(len(m["content"]) for m in user_messages) / len(user_messages) if user_messages else 0,
            "avg_answer_length": sum(len(m["content"]) for m in assistant_messages) / len(assistant_messages) if assistant_messages else 0,
            "estimated_tokens": self.estimate_tokens(),
        }
    
    def __len__(self) -> int:
        """Количество сообщений в контексте"""
        return len(self.messages)
    
    def __repr__(self) -> str:
        return f"ContextManager(session={self.session_id}, messages={len(self.messages)})"

