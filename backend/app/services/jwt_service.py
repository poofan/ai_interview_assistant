"""
JWT Service - [ШТОР + АЗ]
Создание и валидация JWT токенов
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from app.config import get_settings
from app.models.user import User
from app.models.subscription import Subscription

settings = get_settings()


class JWTService:
    """
    Сервис работы с JWT
    Архетипы: ШТОР (безопасность) + АЗ (управление доступом)
    """
    
    @staticmethod
    def create_access_token(user: User, subscription: Optional[Subscription] = None) -> str:
        """
        Создать access token для пользователя
        
        Args:
            user: Пользователь
            subscription: Подписка пользователя
        
        Returns:
            JWT токен
        """
        # Базовые claims
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name or user.email,
            "email_verified": user.email_verified,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        
        # Добавляем информацию о подписке
        if subscription and subscription.is_active:
            payload.update({
                "tier": subscription.tier.value,
                "features": subscription.features,
                "subscription_status": subscription.status.value,
                "subscription_end": subscription.current_period_end.isoformat() if subscription.current_period_end else None
            })
        else:
            # Free tier по умолчанию
            payload.update({
                "tier": "free",
                "features": ["basic_stt", "limited_requests", "standard_context"],
                "subscription_status": "active",
                "subscription_end": None
            })
        
        # Создаем токен
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return token
    
    @staticmethod
    def create_refresh_token(user: User) -> str:
        """
        Создать refresh token
        
        Args:
            user: Пользователь
        
        Returns:
            Refresh токен
        """
        payload = {
            "sub": str(user.id),
            "type": "refresh",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
        }
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return token
    
    @staticmethod
    def decode_token(token: str) -> Optional[Dict]:
        """
        Декодировать и валидировать токен
        
        Args:
            token: JWT токен
        
        Returns:
            Payload токена или None если невалиден
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def create_email_verification_token(user: User) -> str:
        """
        Создать токен для верификации email
        
        Args:
            user: Пользователь
        
        Returns:
            Verification токен
        """
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "type": "email_verification",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=24)  # Действителен 24 часа
        }
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return token
    
    @staticmethod
    def create_password_reset_token(user: User) -> str:
        """
        Создать токен для сброса пароля
        
        Args:
            user: Пользователь
        
        Returns:
            Reset токен
        """
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "type": "password_reset",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=1)  # Действителен 1 час
        }
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return token

