"""
Version Manager - [АЗ + ШТОР]
Управление версиями приложения и проверка обновлений
"""

import requests
import json
from typing import Dict, Optional, Tuple
from loguru import logger
from packaging import version as pkg_version
from datetime import datetime


class VersionManager:
    """
    Менеджер версий приложения
    Архетипы:
    - АЗ: управление доступом к обновлениям
    - ШТОР: безопасная проверка версий
    """
    _instance: Optional['VersionManager'] = None
    
    # Текущая версия приложения (встроенная)
    CURRENT_VERSION = "1.0.0"
    
    # URL для проверки обновлений (будет реализован позже с FastAPI backend)
    UPDATE_CHECK_URL = "https://api.hintsage.com/version/check"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VersionManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Инициализация менеджера версий
        """
        self._current_version = self.CURRENT_VERSION
        self._latest_version: Optional[str] = None
        self._update_available: bool = False
        self._update_info: Dict = {}
        self._check_timeout = 5  # Таймаут для проверки обновлений (секунды)
    
    def get_current_version(self) -> str:
        """
        [АЗ] - Получить текущую версию приложения
        
        Returns:
            Строка с версией (например, "1.0.0")
        """
        return self._current_version
    
    def check_for_updates(self, skip_network: bool = False) -> Tuple[bool, Optional[str], Dict]:
        """
        [ШТОР + АЗ] - Проверить наличие обновлений
        
        Args:
            skip_network: Пропустить сетевую проверку (для offline режима)
        
        Returns:
            Tuple[bool, Optional[str], Dict]: (есть_обновление, новая_версия, информация)
        """
        if skip_network:
            logger.debug("Пропуск сетевой проверки обновлений (offline режим)")
            return False, None, {}
        
        try:
            logger.info("🔍 Проверка обновлений...")
            
            # Отправляем текущую версию на сервер
            payload = {
                "current_version": self._current_version,
                "platform": "windows",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            response = requests.post(
                self.UPDATE_CHECK_URL,
                json=payload,
                timeout=self._check_timeout
            )
            
            if response.status_code == 200:
                update_data = response.json()
                
                latest_version = update_data.get("latest_version", self._current_version)
                self._latest_version = latest_version
                
                # Сравниваем версии
                self._update_available = self._compare_versions(
                    self._current_version,
                    latest_version
                )
                
                if self._update_available:
                    self._update_info = {
                        "version": latest_version,
                        "release_date": update_data.get("release_date", ""),
                        "download_url": update_data.get("download_url", ""),
                        "changelog": update_data.get("changelog", []),
                        "critical": update_data.get("critical", False),
                        "min_version": update_data.get("min_version", "0.0.0")
                    }
                    
                    logger.info(f"✨ Доступно обновление: {latest_version}")
                    return True, latest_version, self._update_info
                else:
                    logger.info("✅ Используется актуальная версия")
                    return False, latest_version, {}
            
            elif response.status_code == 404:
                # Сервер обновлений не найден - работаем в offline режиме
                logger.warning("⚠️ Сервер обновлений недоступен (404)")
                return False, None, {}
            
            else:
                logger.warning(f"⚠️ Ошибка проверки обновлений: {response.status_code}")
                return False, None, {}
                
        except requests.exceptions.Timeout:
            logger.warning("⏱️ Таймаут при проверке обновлений")
            return False, None, {}
        
        except requests.exceptions.ConnectionError:
            logger.warning("🌐 Нет подключения к серверу обновлений")
            return False, None, {}
        
        except Exception as e:
            logger.error(f"❌ Ошибка при проверке обновлений: {e}")
            return False, None, {}
    
    def _compare_versions(self, current: str, latest: str) -> bool:
        """
        [АЗ] - Сравнить версии
        
        Args:
            current: Текущая версия
            latest: Последняя версия
        
        Returns:
            True если доступно обновление
        """
        try:
            return pkg_version.parse(latest) > pkg_version.parse(current)
        except Exception as e:
            logger.warning(f"⚠️ Ошибка сравнения версий: {e}")
            return False
    
    def is_version_supported(self, min_version: str) -> bool:
        """
        [АЗ] - Проверить, поддерживается ли текущая версия
        
        Args:
            min_version: Минимальная поддерживаемая версия
        
        Returns:
            True если версия поддерживается
        """
        try:
            return pkg_version.parse(self._current_version) >= pkg_version.parse(min_version)
        except Exception as e:
            logger.warning(f"⚠️ Ошибка проверки поддержки версии: {e}")
            return True  # По умолчанию считаем, что версия поддерживается
    
    def get_update_info(self) -> Dict:
        """
        [АЗ] - Получить информацию об обновлении
        
        Returns:
            Словарь с информацией об обновлении
        """
        return self._update_info
    
    def is_critical_update_available(self) -> bool:
        """
        [ШТОР + АЗ] - Проверить, доступно ли критическое обновление
        
        Returns:
            True если доступно критическое обновление
        """
        return self._update_available and self._update_info.get("critical", False)
    
    def get_version_info(self) -> Dict:
        """
        [АЗ] - Получить полную информацию о версии
        
        Returns:
            Словарь с информацией о текущей и последней версии
        """
        return {
            "current_version": self._current_version,
            "latest_version": self._latest_version,
            "update_available": self._update_available,
            "update_info": self._update_info
        }
    
    def format_changelog(self) -> str:
        """
        [АЗ] - Форматировать changelog для отображения
        
        Returns:
            Форматированный changelog
        """
        if not self._update_info or "changelog" not in self._update_info:
            return "Нет информации об изменениях"
        
        changelog = self._update_info["changelog"]
        if isinstance(changelog, list):
            return "\n".join([f"• {item}" for item in changelog])
        else:
            return str(changelog)


def get_version_manager() -> VersionManager:
    """
    Получить глобальный экземпляр VersionManager
    """
    return VersionManager()

