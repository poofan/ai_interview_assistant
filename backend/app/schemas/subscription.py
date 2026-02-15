"""
Subscription Schemas - [АЗ + ДОБРО]
Pydantic модели для подписок
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SubscriptionResponse(BaseModel):
    """Ответ с данными подписки"""
    id: str
    tier: str
    status: str
    features: List[str]
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    is_active: bool
    
    class Config:
        from_attributes = True

