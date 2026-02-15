"""
User Service - [АЗ + ДОБРО]
Управление пользователями
"""

from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Сервис работы с пользователями"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Получить пользователя по email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Получить пользователя по ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, email: str, password: str, name: Optional[str] = None) -> User:
        """Создать нового пользователя"""
        hashed_password = pwd_context.hash(password)
        
        user = User(
            email=email,
            password_hash=hashed_password,
            name=name,
            email_verified=False
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверить пароль"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def update_user(self, user: User, **kwargs) -> User:
        """Обновить пользователя"""
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        
        return user

