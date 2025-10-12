"""
Auth Middleware - [ШТОР + АЗ]
Middleware для проверки JWT токенов
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.jwt_service import JWTService
from app.services.user_service import UserService
from app.models.user import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Получить текущего пользователя из JWT токена
    
    Args:
        credentials: HTTP Bearer credentials
        db: Database session
    
    Returns:
        User: Текущий пользователь
    
    Raises:
        HTTPException: Если токен невалиден или пользователь не найден
    """
    token = credentials.credentials
    
    # Декодируем токен
    payload = JWTService.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Получаем user_id из токена
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Получаем пользователя из БД
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь деактивирован"
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Получить текущего активного пользователя
    
    Args:
        current_user: Текущий пользователь
    
    Returns:
        User: Активный пользователь
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неактивный пользователь"
        )
    return current_user

