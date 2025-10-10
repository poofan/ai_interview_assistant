"""
Config Manager - [ДОБРО + АЗ]
Управление конфигурацией и безопасное хранение API ключей
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from loguru import logger


class ConfigManager:
    """
    Менеджер конфигурации
    Архетипы:
    - ДОБРО: организация настроек
    - АЗ: управление учетными данными (API ключи)
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Инициализация менеджера конфигурации
        
        Args:
            config_path: Путь к файлу конфигурации
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.encryption_key: Optional[bytes] = None
        self._init_encryption()
        self.load_config()
    
    def _init_encryption(self) -> None:
        """
        [АЗ + ШТОР] - Инициализация шифрования для API ключей
        """
        key_file = Path(".encryption_key")
        
        if key_file.exists():
            with open(key_file, "rb") as f:
                self.encryption_key = f.read()
        else:
            self.encryption_key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(self.encryption_key)
            # Скрыть файл (Windows)
            try:
                os.system(f'attrib +h "{key_file}"')
            except Exception as e:
                logger.warning(f"Не удалось скрыть файл ключа: {e}")
    
    def load_config(self) -> Dict[str, Any]:
        """
        [ВЕДИ + ДОБРО] - Загрузить конфигурацию из файла
        
        Returns:
            Словарь с конфигурацией
        """
        if not self.config_path.exists():
            logger.warning(f"Конфигурационный файл {self.config_path} не найден")
            logger.info("Копируем config.example.yaml -> config.yaml")
            
            example_path = Path("config.example.yaml")
            if example_path.exists():
                import shutil
                shutil.copy(example_path, self.config_path)
            else:
                logger.error("Файл config.example.yaml не найден!")
                raise FileNotFoundError("Необходим файл config.example.yaml")
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f) or {}
            
            logger.info(f"Конфигурация загружена из {self.config_path}")
            return self.config
        
        except Exception as e:
            logger.error(f"Ошибка загрузки конфигурации: {e}")
            raise
    
    def save_config(self) -> None:
        """
        [ПАМЯТЬ + ДОБРО] - Сохранить конфигурацию в файл
        """
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
            
            logger.info(f"Конфигурация сохранена в {self.config_path}")
        
        except Exception as e:
            logger.error(f"Ошибка сохранения конфигурации: {e}")
            raise
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        [ВЕДИ] - Получить значение по пути (например, "openai.api_key")
        
        Args:
            key_path: Путь к значению через точку
            default: Значение по умолчанию
        
        Returns:
            Значение из конфигурации
        """
        keys = key_path.split(".")
        value = self.config
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> None:
        """
        [ДОБРО] - Установить значение по пути
        
        Args:
            key_path: Путь к значению через точку
            value: Новое значение
        """
        keys = key_path.split(".")
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        logger.debug(f"Установлено значение {key_path} = {value}")
    
    def encrypt_api_key(self, api_key: str) -> str:
        """
        [ТАЙНА + АЗ] - Зашифровать API ключ
        
        Args:
            api_key: Открытый API ключ
        
        Returns:
            Зашифрованный ключ (base64)
        """
        if not self.encryption_key:
            raise ValueError("Ключ шифрования не инициализирован")
        
        fernet = Fernet(self.encryption_key)
        encrypted = fernet.encrypt(api_key.encode())
        return encrypted.decode()
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """
        [ТАЙНА + АЗ] - Расшифровать API ключ
        
        Args:
            encrypted_key: Зашифрованный ключ
        
        Returns:
            Расшифрованный API ключ
        """
        if not self.encryption_key:
            raise ValueError("Ключ шифрования не инициализирован")
        
        fernet = Fernet(self.encryption_key)
        decrypted = fernet.decrypt(encrypted_key.encode())
        return decrypted.decode()
    
    def get_openai_api_key(self) -> str:
        """
        [АЗ] - Получить OpenAI API ключ (с расшифровкой если нужно)
        
        Returns:
            OpenAI API ключ
        """
        api_key = self.get("openai.api_key", "")
        
        if not api_key:
            raise ValueError("OpenAI API ключ не настроен в config.yaml")
        
        # Проверяем, зашифрован ли ключ
        if self.get("security.encrypt_api_key", False):
            try:
                api_key = self.decrypt_api_key(api_key)
            except Exception as e:
                logger.error(f"Ошибка расшифровки API ключа: {e}")
                raise
        
        return api_key
    
    def validate_config(self) -> bool:
        """
        [ШТОР + ЧЕЛО] - Валидировать конфигурацию
        
        Returns:
            True если конфигурация валидна
        """
        required_fields = [
            "openai.api_key",
            "openai.model",
            "stt.default_engine",
        ]
        
        for field in required_fields:
            value = self.get(field)
            if not value:
                logger.error(f"Обязательное поле {field} не заполнено")
                return False
        
        logger.info("[OK] Конфигурация валидна")
        return True


# Singleton instance
_config_instance: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """
    Получить глобальный экземпляр ConfigManager
    
    Returns:
        ConfigManager instance
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = ConfigManager()
    
    return _config_instance


