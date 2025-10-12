"""
User Schemas - [АЗ + ДОБРО]
Pydantic модели для пользователей
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserResponse(BaseModel):
    """Ответ с данными пользователя"""
    id: str
    email: EmailStr
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    email_verified: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Обновление профиля пользователя"""
    name: Optional[str] = None
    avatar_url: Optional[str] = None

