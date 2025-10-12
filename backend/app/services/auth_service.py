"""
Auth Service - [ШТОР + АЗ]
Аутентификация и авторизация
"""

from sqlalchemy.orm import Session
from typing import Optional, Tuple
from app.models.user import User
from app.models.subscription import Subscription, SubscriptionTier, SubscriptionStatus
from app.services.user_service import UserService
from app.services.jwt_service import JWTService


class AuthService:
    """Сервис аутентификации"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
        self.jwt_service = JWTService()
    
    def register(self, email: str, password: str, name: Optional[str] = None) -> Tuple[User, str, str]:
        """
        Регистрация нового пользователя
        
        Returns:
            (user, access_token, refresh_token)
        """
        # Проверяем существование
        existing_user = self.user_service.get_user_by_email(email)
        if existing_user:
            raise ValueError("Пользователь с таким email уже существует")
        
        # Создаем пользователя
        user = self.user_service.create_user(email, password, name)
        
        # Создаем FREE подписку
        subscription = Subscription(
            user_id=user.id,
            tier=SubscriptionTier.FREE,
            status=SubscriptionStatus.ACTIVE
        )
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        
        # Генерируем токены
        access_token = self.jwt_service.create_access_token(user, subscription)
        refresh_token = self.jwt_service.create_refresh_token(user)
        
        return user, access_token, refresh_token
    
    def login(self, email: str, password: str) -> Tuple[User, str, str]:
        """
        Вход пользователя
        
        Returns:
            (user, access_token, refresh_token)
        """
        # Получаем пользователя
        user = self.user_service.get_user_by_email(email)
        if not user:
            raise ValueError("Неверный email или пароль")
        
        # Проверяем пароль
        if not self.user_service.verify_password(password, user.password_hash):
            raise ValueError("Неверный email или пароль")
        
        # Получаем подписку
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user.id
        ).first()
        
        # Генерируем токены
        access_token = self.jwt_service.create_access_token(user, subscription)
        refresh_token = self.jwt_service.create_refresh_token(user)
        
        return user, access_token, refresh_token
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Обновить access token используя refresh token
        
        Returns:
            Новый access_token
        """
        # Декодируем refresh token
        payload = self.jwt_service.decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise ValueError("Невалидный refresh token")
        
        # Получаем пользователя
        user_id = payload.get("sub")
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        
        # Получаем подписку
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user.id
        ).first()
        
        # Генерируем новый access token
        access_token = self.jwt_service.create_access_token(user, subscription)
        
        return access_token

