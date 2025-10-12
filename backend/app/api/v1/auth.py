"""
Auth API Endpoints - [ШТОР + АЗ]
Эндпоинты аутентификации
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя
    
    - **email**: Email пользователя
    - **password**: Пароль (минимум 8 символов)
    - **name**: Имя пользователя (опционально)
    
    Returns:
        JWT токены и данные пользователя
    """
    auth_service = AuthService(db)
    
    try:
        user, access_token, refresh_token = auth_service.register(
            email=request.email,
            password=request.password,
            name=request.name
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.from_orm(user)
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Вход пользователя
    
    - **email**: Email пользователя
    - **password**: Пароль
    
    Returns:
        JWT токены и данные пользователя
    """
    auth_service = AuthService(db)
    
    try:
        user, access_token, refresh_token = auth_service.login(
            email=request.email,
            password=request.password
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.from_orm(user)
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/refresh", response_model=dict)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Обновить access token используя refresh token
    
    - **refresh_token**: Refresh token
    
    Returns:
        Новый access token
    """
    auth_service = AuthService(db)
    
    try:
        access_token = auth_service.refresh_access_token(request.refresh_token)
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

