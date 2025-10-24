"""
LLM Client - [РЦИ + ИЖЕ]
Клиент для взаимодействия с OpenAI API
"""

import openai
from typing import List, Dict, Optional, AsyncIterator
from loguru import logger
import asyncio
from datetime import datetime


class LLMClient:
    """
    Клиент для работы с OpenAI API
    Архетипы:
    - РЦИ: внешний запрос к API
    - ИЖЕ: передача данных
    - МЫСЛЕТЕ: генерация ответа
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        max_tokens: int = 500,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ):
        """
        Инициализация LLM клиента
        
        Args:
            api_key: OpenAI API ключ
            model: Модель GPT (gpt-4, gpt-4o, gpt-4-turbo)
            max_tokens: Максимум токенов в ответе
            temperature: Температура генерации (0-2)
            system_prompt: Системный промпт
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt or (
            "Ты - профессиональный технический консультант. "
            "Давай краткие, точные и структурированные ответы на вопросы собеседований. "
            "Используй примеры кода когда уместно. Отвечай на русском языке."
        )
        
        # Настройка клиента OpenAI
        self.client = openai.OpenAI(api_key=self.api_key)
        
        logger.info(f"[OK] LLM Client инициализирован (модель: {self.model})")
    
    def generate_response(
        self,
        question: str,
        context: Optional[List[Dict[str, str]]] = None,
        stream: bool = False
    ) -> str:
        """
        [РЦИ + МЫСЛЕТЕ] - Сгенерировать ответ на вопрос
        
        Args:
            question: Вопрос для ответа
            context: История диалога (опционально)
            stream: Потоковая генерация
        
        Returns:
            Сгенерированный ответ
        """
        try:
            messages = self._prepare_messages(question, context)
            
            logger.debug(f"Отправка запроса к OpenAI (модель: {self.model})")
            
            if stream:
                return self._generate_stream(messages)
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                
                answer = response.choices[0].message.content.strip()
                
                logger.info(f"[OK] Получен ответ от OpenAI ({len(answer)} символов)")
                logger.debug(f"Использовано токенов: {response.usage.total_tokens}")
                
                return answer
        
        except openai.AuthenticationError:
            logger.error("[ERROR] Ошибка аутентификации OpenAI - проверьте API ключ")
            raise
        
        except openai.RateLimitError as e:
            logger.warning("[WARNING] Rate limit превышен, ждем 60 сек...")
            import time
            time.sleep(60)
            # Retry один раз
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                answer = response.choices[0].message.content.strip()
                logger.info(f"[OK] Ответ получен после retry ({len(answer)} символов)")
                return answer
            except Exception as retry_error:
                logger.error(f"[ERROR] Ошибка после retry: {retry_error}")
                raise
        
        except openai.APIError as e:
            logger.error(f"[ERROR] Ошибка API OpenAI: {e}")
            raise
        
        except Exception as e:
            logger.error(f"[ERROR] Неожиданная ошибка при генерации ответа: {e}")
            raise
    
    async def generate_response_async(
        self,
        question: str,
        context: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        [РЦИ + ИЖЕ] - Асинхронная генерация ответа
        
        Args:
            question: Вопрос
            context: История диалога
        
        Returns:
            Сгенерированный ответ
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.generate_response,
            question,
            context,
            False
        )
    
    def _generate_stream(self, messages: List[Dict[str, str]]) -> str:
        """
        [ИЖЕ] - Потоковая генерация (для будущего использования)
        
        Args:
            messages: Сообщения для отправки
        
        Returns:
            Полный ответ
        """
        full_response = ""
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
            
            logger.info(f"[OK] Получен потоковый ответ ({len(full_response)} символов)")
            return full_response
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка потоковой генерации: {e}")
            raise
    
    def _prepare_messages(
        self,
        question: str,
        context: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, str]]:
        """
        [ДОБРО + ПАМЯТЬ] - Подготовить сообщения для отправки
        
        Args:
            question: Текущий вопрос
            context: История диалога
        
        Returns:
            Список сообщений
        """
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Добавляем контекст если есть
        if context:
            messages.extend(context)
        
        # Добавляем текущий вопрос
        messages.append({"role": "user", "content": question})
        
        return messages
    
    def estimate_tokens(self, text: str) -> int:
        """
        [МЫСЛЕТЕ] - Примерная оценка количества токенов
        
        Args:
            text: Текст для оценки
        
        Returns:
            Примерное количество токенов
        """
        # Простая эвристика: 1 токен ≈ 4 символа для английского, ≈ 2 для русского
        # Более точная оценка требует tiktoken
        return len(text) // 3
    
    def validate_api_key(self) -> bool:
        """
        [АЗ + РЦИ] - Проверить валидность API ключа
        
        Returns:
            True если ключ валиден
        """
        try:
            # Делаем минимальный запрос для проверки
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5
            )
            
            logger.info("[OK] OpenAI API ключ валиден")
            return True
        
        except openai.AuthenticationError:
            logger.error("[ERROR] Неверный OpenAI API ключ")
            return False
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка проверки API ключа: {e}")
            return False
    
    def change_model(self, model: str) -> None:
        """
        [ДОБРО] - Изменить модель GPT
        
        Args:
            model: Новая модель (gpt-4, gpt-4o, etc.)
        """
        old_model = self.model
        self.model = model
        logger.info(f"Модель изменена: {old_model} -> {model}")
    
    def update_system_prompt(self, prompt: str) -> None:
        """
        [СЛОВО + ДОБРО] - Обновить системный промпт
        
        Args:
            prompt: Новый системный промпт
        """
        self.system_prompt = prompt
        logger.info("Системный промпт обновлен")

