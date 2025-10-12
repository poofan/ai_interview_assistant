"""
Backend Configuration - [АЗ + ШТОР]
Настройки приложения и переменные окружения
"""

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """
    Настройки приложения
    Архетипы: АЗ (управление доступом) + ШТОР (безопасность)
    """
    
    # Основные настройки
    APP_NAME: str = "Hintsage Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/hintsage"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    JWT_SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 дней
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 дней
    
    # Security
    BCRYPT_ROUNDS: int = 12
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://smartsobes.ru",
        "https://www.smartsobes.ru"
    ]
    
    # Email
    SMTP_HOST: str = "smtp.yandex.ru"  # Для РФ рекомендую Yandex или Mail.ru
    SMTP_PORT: int = 587
    SMTP_USER: str = "noreply@smartsobes.ru"
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "Hintsage <noreply@smartsobes.ru>"
    
    # Банк Точка
    TOCHKA_API_URL: str = "https://enter.tochka.com/uapi"
    TOCHKA_BEARER_TOKEN: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJjZGQxNjE3ZWQwNGQ2ZTAzMzhhZWU4MThiNmQ3NDU0NCJ9.gQgaJO3FoI0eSWyQOXHMYVIfAhlKTqbbDrLXW0sTkB-csYu0W0qP_Pr2KUF3YbLRbIJrNTEwsy4-zsKTlVrzjH5QtZu1QBa1jPCKCpn7k4hGb0L7SiXtPaDdoFSrTzL6zzv0wVZP0e9pQfbRARovf8XHv9lP5HT-Q1InSQIiJjnVVwd8ymMgjYDl8CKQDC3Zkki2R-OpiKyJAubXeLlIjbgqwIANDJwdvbZy0Magu3trrRl-hh2vvSxRxYWRlLf5a8w4PibHPpbzC4Ig8zm-HplmYgp3U9HeaqpEAqbARNRlqQUsVUrQgkHUpFToGX_3SvOGkO4eeF5HsXzDO-qV4J9C03mor8cFNHftUriAXrIqMCMfER3JfE2dGgqNyYYPoRAW-oqvoreDl2skaZiEHEizSoPKMILXC3YJ8fSdZ8BMJ1mNzTlUqpltxNpHRKmHvmTaGr3ushIJqeS8kay_0BXUbt-fRsZZk25RSIVTYbOhUvz7CIKXF8-Nvg8xQilE"
    TOCHKA_CUSTOMER_CODE: str = "305047981"  # Код покупателя
    TOCHKA_MERCHANT_ID: str = "200000000021710"  # Merchant ID
    TOCHKA_CLIENT_ID: str = "cdd1617ed04d6e0338aee818b6d74544"  # Client ID
    TOCHKA_TAX_SYSTEM_CODE: str = "osn"  # Система налогообложения
    
    # Subscription Tiers Pricing (в рублях)
    PRICE_PRO_MONTHLY: float = 1499.00  # ~$19 по курсу
    PRICE_PRO_YEARLY: float = 14990.00  # Скидка 17%
    PRICE_ENTERPRISE_MONTHLY: float = 7490.00  # ~$99
    PRICE_ENTERPRISE_YEARLY: float = 74900.00  # Скидка 17%
    
    # App Version Control
    MIN_SUPPORTED_APP_VERSION: str = "1.0.0"
    LATEST_APP_VERSION: str = "1.0.0"
    APP_DOWNLOAD_URL: str = "https://smartsobes.ru/download/Hintsage.exe"
    
    # OAuth (будущее)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    
    # Frontend URL
    FRONTEND_URL: str = "https://smartsobes.ru"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Получить настройки приложения (с кэшированием)
    """
    return Settings()

