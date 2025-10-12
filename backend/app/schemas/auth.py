"""
Auth Schemas - [ШТОР + АЗ]
Pydantic модели для аутентификации
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class RegisterRequest(BaseModel):
    """Запрос на регистрацию"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    name: Optional[str] = Field(None, max_length=255)


class LoginRequest(BaseModel):
    """Запрос на вход"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Ответ с токенами"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class RefreshTokenRequest(BaseModel):
    """Запрос на обновление токена"""
    refresh_token: str


# Forward reference для UserResponse
from app.schemas.user import UserResponse
TokenResponse.model_rebuild()

