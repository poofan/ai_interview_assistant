"""
Payment Schemas - [АЗ + ДОБРО]
Pydantic модели для платежей
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentCreateRequest(BaseModel):
    """Запрос на создание платежа"""
    tier: str  # "pro" или "enterprise"
    period: str  # "monthly" или "yearly"


class PaymentResponse(BaseModel):
    """Ответ с данными платежа"""
    operation_id: str
    payment_link: str
    amount: float
    purpose: str
    status: str


class PaymentStatusResponse(BaseModel):
    """Статус платежа"""
    operation_id: str
    status: str
    amount: float
    paid_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

