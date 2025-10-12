"""
API Keys Manager - [ТАЙНА + АЗ]
Управление API ключами с встроенными ключами
"""

import requests
import time
from typing import Dict, Optional, List, Any
from loguru import logger


class APIKeyManager:
    """
    Менеджер API ключей с встроенными ключами
    Архетипы:
    - ТАЙНА: защита ключей
    - АЗ: управление доступом
    """
    
    def __init__(self):
        """
        Инициализация менеджера API ключей
        """
        # Встроенные API ключи (защищены PyInstaller)
        # ВАЖНО: Замените на ваши реальные API ключи OpenAI
        self._hardcoded_keys = {
            "primary": "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",  # Замените на ваш ключ
            "backup": "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",   # Резервный ключ (опционально)
        }
        
        # Активный ключ
        self._active_key = "primary"
        
        # Кэш проверки ключей
        self._key_validation_cache: Dict[str, Dict[str, Any]] = {}
        
        # Настройки проверки
        self._validation_timeout = 30  # секунд
        self._cache_duration = 3600    # секунд (1 час)
    
    def get_active_key(self) -> str:
        """
        Получить активный API ключ
        
        Returns:
            Активный API ключ
        """
        return self._hardcoded_keys[self._active_key]
    
    def get_all_keys(self) -> Dict[str, str]:
        """
        Получить все доступные ключи
        
        Returns:
            Словарь с ключами
        """
        return self._hardcoded_keys.copy()
    
    def switch_to_key(self, key_name: str) -> bool:
        """
        Переключиться на другой ключ
        
        Args:
            key_name: Имя ключа (primary, backup)
            
        Returns:
            True если переключение успешно
        """
        if key_name not in self._hardcoded_keys:
            logger.error(f"Ключ {key_name} не найден")
            return False
        
        # Проверяем ключ перед переключением
        if self.validate_key(self._hardcoded_keys[key_name]):
            self._active_key = key_name
            logger.info(f"Переключились на ключ: {key_name}")
            return True
        else:
            logger.error(f"Ключ {key_name} не прошел валидацию")
            return False
    
    def validate_key(self, api_key: str) -> bool:
        """
        Проверить валидность API ключа
        
        Args:
            api_key: API ключ для проверки
            
        Returns:
            True если ключ валиден
        """
        # Проверяем кэш
        if api_key in self._key_validation_cache:
            cache_entry = self._key_validation_cache[api_key]
            if time.time() - cache_entry["timestamp"] < self._cache_duration:
                return cache_entry["valid"]
        
        # Проверяем ключ через OpenAI API
        try:
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                timeout=self._validation_timeout
            )
            
            is_valid = response.status_code == 200
            
            # Анализируем ошибку для детального сообщения
            error_details = {
                "status_code": response.status_code,
                "error_type": "unknown",
                "error_message": "Unknown error",
                "suggestion": "Попробуйте перезапустить приложение"
            }
            
            # Обрабатываем все коды ошибок (не только 403)
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    error_info = error_data.get("error", {})
                    error_code = error_info.get("code", "")
                    error_message = error_info.get("message", f"HTTP {response.status_code}")
                    
                    error_details.update({
                        "error_type": error_code if error_code else f"http_{response.status_code}",
                        "error_message": error_message
                    })
                    
                    # Определяем причину и решение
                    if "unsupported_country" in error_code or response.status_code == 451:
                        error_details["suggestion"] = "Включите VPN для доступа к OpenAI API"
                        error_details["error_type"] = "unsupported_country_region_territory"
                    elif "invalid_api_key" in error_code or response.status_code == 401:
                        error_details["suggestion"] = "API ключ недействителен или истек"
                        error_details["error_type"] = "invalid_api_key"
                    elif "quota_exceeded" in error_code or response.status_code == 429:
                        error_details["suggestion"] = "Превышена квота API, пополните баланс"
                        error_details["error_type"] = "quota_exceeded"
                    elif response.status_code == 403:
                        error_details["suggestion"] = "Доступ запрещен. Включите VPN и попробуйте снова"
                        error_details["error_type"] = "unsupported_country_region_territory"
                    elif response.status_code == 405:
                        error_details["suggestion"] = "Проблема с запросом. Возможно, требуется VPN"
                        error_details["error_type"] = "unsupported_country_region_territory"
                    else:
                        error_details["suggestion"] = "Проверьте подключение к интернету и VPN"
                        
                except Exception as e:
                    logger.debug(f"Не удалось распарсить ответ: {e}")
                    error_details["error_message"] = f"HTTP {response.status_code}: {response.text[:100]}"
                    if response.status_code in [403, 405, 451]:
                        error_details["suggestion"] = "Включите VPN для доступа к OpenAI API"
                        error_details["error_type"] = "unsupported_country_region_territory"
                    else:
                        error_details["suggestion"] = "Проверьте подключение к интернету"
            
            # Сохраняем в кэш с детальной информацией
            self._key_validation_cache[api_key] = {
                "valid": is_valid,
                "timestamp": time.time(),
                "error_details": error_details
            }
            
            if is_valid:
                logger.info("✅ API ключ валиден")
            else:
                logger.error(f"❌ API ключ невалиден: {response.status_code}")
                logger.error(f"Ошибка: {error_details['error_message']}")
                logger.error(f"Решение: {error_details['suggestion']}")
            
            return is_valid
            
        except requests.exceptions.Timeout:
            logger.error("⏱️ Таймаут при проверке API ключа")
            return False
        except requests.exceptions.ConnectionError:
            logger.error("🌐 Ошибка подключения при проверке API ключа")
            return False
        except Exception as e:
            logger.error(f"❌ Ошибка при проверке API ключа: {e}")
            return False
    
    def validate_active_key(self) -> bool:
        """
        Проверить активный API ключ
        
        Returns:
            True если активный ключ валиден
        """
        active_key = self.get_active_key()
        return self.validate_key(active_key)
    
    def auto_fallback(self) -> bool:
        """
        Автоматическое переключение на резервный ключ
        
        Returns:
            True если найдены рабочие ключи
        """
        logger.info("🔄 Попытка автоматического переключения ключей...")
        
        for key_name, api_key in self._hardcoded_keys.items():
            if key_name == self._active_key:
                continue  # Пропускаем текущий ключ
            
            logger.info(f"Проверяем ключ: {key_name}")
            if self.validate_key(api_key):
                self._active_key = key_name
                logger.info(f"✅ Переключились на рабочий ключ: {key_name}")
                return True
        
        logger.error("❌ Не найдено рабочих API ключей")
        return False
    
    def get_last_error_details(self) -> Dict[str, Any]:
        """
        Получить детали последней ошибки
        
        Returns:
            Словарь с деталями ошибки
        """
        active_key = self.get_active_key()
        if active_key in self._key_validation_cache:
            cache_entry = self._key_validation_cache[active_key]
            if not cache_entry["valid"] and "error_details" in cache_entry:
                return cache_entry["error_details"]
        
        # Возвращаем общую ошибку
        return {
            "status_code": "unknown",
            "error_type": "no_valid_keys",
            "error_message": "Все API ключи недоступны",
            "suggestion": "Проверьте подключение к интернету и настройки VPN"
        }
    
    def get_key_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Получить статус всех ключей
        
        Returns:
            Словарь со статусом ключей
        """
        status = {}
        
        for key_name, api_key in self._hardcoded_keys.items():
            if api_key in self._key_validation_cache:
                cache_entry = self._key_validation_cache[api_key]
                if time.time() - cache_entry["timestamp"] < self._cache_duration:
                    status[key_name] = {
                        "valid": cache_entry["valid"],
                        "last_checked": cache_entry["timestamp"],
                        "status_code": cache_entry.get("status_code", "unknown"),
                        "is_active": key_name == self._active_key
                    }
                    continue
            
            # Если нет кэша, проверяем ключ
            is_valid = self.validate_key(api_key)
            status[key_name] = {
                "valid": is_valid,
                "last_checked": time.time(),
                "status_code": "unknown",
                "is_active": key_name == self._active_key
            }
        
        return status
    
    def clear_cache(self) -> None:
        """
        Очистить кэш валидации ключей
        """
        self._key_validation_cache.clear()
        logger.info("🧹 Кэш валидации ключей очищен")
    
    def update_key_from_server(self, key_name: str, new_key: str) -> bool:
        """
        Обновить ключ с сервера (будущая функция)
        
        Args:
            key_name: Имя ключа для обновления
            new_key: Новый ключ
            
        Returns:
            True если обновление успешно
        """
        # TODO: Реализовать обновление ключей с сервера
        logger.warning(f"Обновление ключа {key_name} с сервера не реализовано")
        return False


# Глобальный экземпляр
_api_key_manager: Optional[APIKeyManager] = None


def get_api_key_manager() -> APIKeyManager:
    """
    Получить глобальный экземпляр APIKeyManager
    
    Returns:
        APIKeyManager instance
    """
    global _api_key_manager
    
    if _api_key_manager is None:
        _api_key_manager = APIKeyManager()
    
    return _api_key_manager


def get_openai_api_key() -> str:
    """
    Быстрая функция для получения API ключа OpenAI
    
    Returns:
        API ключ OpenAI
    """
    manager = get_api_key_manager()
    return manager.get_active_key()
