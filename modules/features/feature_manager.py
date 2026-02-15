"""
Feature Manager - [АЗ + ДОБРО]
Управление доступными фичами на основе подписки
"""

from typing import List, Dict
from loguru import logger


class FeatureManager:
    """
    Менеджер фич приложения
    Архетипы: АЗ (контроль доступа) + ДОБРО (предоставление услуг)
    """
    
    # Определение фич по тарифам
    TIER_FEATURES = {
        "free": [
            "basic_stt",  # Только Vosk
            "limited_requests",  # 5 запросов/час
            "standard_context",  # Стандартный контекст (10 сообщений)
        ],
        "pro": [
            "advanced_stt",  # Whisper GPU
            "unlimited_requests",  # Без ограничений
            "extended_context",  # Расширенный контекст (30 сообщений)
            "custom_prompts",  # Кастомные промпты
            "screenshot_ocr",  # OCR скриншотов
            "priority_support",  # Приоритетная поддержка
        ],
        "enterprise": [
            "advanced_stt",
            "unlimited_requests",
            "extended_context",
            "custom_prompts",
            "screenshot_ocr",
            "priority_support",
            "team_sharing",  # Командный доступ (будущее)
            "custom_integrations",  # Кастомные интеграции
            "dedicated_support",  # Выделенная поддержка
        ],
    }
    
    def __init__(self, tier: str = "free", features: List[str] = None):
        """
        Инициализация Feature Manager
        
        Args:
            tier: Тариф подписки (free, pro, enterprise)
            features: Список доступных фич (из JWT), если None - используются по tier
        """
        self.tier = tier.lower()
        
        # Если фичи явно переданы из JWT - используем их
        # Иначе берем стандартные для тарифа
        if features:
            self.features = features
        else:
            self.features = self.TIER_FEATURES.get(self.tier, self.TIER_FEATURES["free"])
        
        logger.info(f"🎯 Feature Manager инициализирован (tier: {self.tier}, features: {len(self.features)})")
    
    def is_feature_enabled(self, feature: str) -> bool:
        """
        Проверить доступность фичи
        
        Args:
            feature: Название фичи
        
        Returns:
            True если фича доступна
        """
        return feature in self.features
    
    def get_stt_engine(self) -> str:
        """
        Определить какой STT движок использовать
        
        Returns:
            "whisper" для PRO+, "vosk" для FREE
        """
        if self.is_feature_enabled("advanced_stt"):
            return "whisper"
        return "vosk"
    
    def get_max_requests_per_hour(self) -> int:
        """
        Получить лимит запросов в час
        
        Returns:
            Количество запросов или -1 для unlimited
        """
        if self.is_feature_enabled("unlimited_requests"):
            return -1  # Без ограничений
        return 5  # FREE tier
    
    def get_context_window_size(self) -> int:
        """
        Получить размер окна контекста
        
        Returns:
            Количество сообщений в контексте
        """
        if self.is_feature_enabled("extended_context"):
            return 30  # PRO+
        return 10  # FREE
    
    def can_use_screenshot_ocr(self) -> bool:
        """Доступен ли OCR скриншотов"""
        return self.is_feature_enabled("screenshot_ocr")
    
    def can_use_custom_prompts(self) -> bool:
        """Доступны ли кастомные промпты"""
        return self.is_feature_enabled("custom_prompts")
    
    def get_feature_restrictions(self) -> Dict[str, any]:
        """
        Получить все ограничения для текущего тарифа
        
        Returns:
            Словарь с ограничениями
        """
        return {
            "tier": self.tier,
            "stt_engine": self.get_stt_engine(),
            "max_requests_per_hour": self.get_max_requests_per_hour(),
            "context_window": self.get_context_window_size(),
            "ocr_enabled": self.can_use_screenshot_ocr(),
            "custom_prompts_enabled": self.can_use_custom_prompts(),
            "features": self.features
        }
    
    def get_upgrade_message(self) -> str:
        """
        Получить сообщение для апгрейда подписки
        
        Returns:
            Текст сообщения
        """
        if self.tier == "free":
            return (
                "🔓 Upgrade до PRO для доступа к:\n"
                "• Whisper GPU (точное распознавание)\n"
                "• Безлимитным запросам\n"
                "• Расширенному контексту\n"
                "• OCR скриншотов\n\n"
                "Цена: 1499₽/месяц"
            )
        elif self.tier == "pro":
            return (
                "🚀 Upgrade до ENTERPRISE для:\n"
                "• Командного доступа\n"
                "• Кастомных интеграций\n"
                "• Выделенной поддержки\n\n"
                "Цена: 7490₽/месяц"
            )
        else:
            return "✨ У вас максимальный тариф!"

