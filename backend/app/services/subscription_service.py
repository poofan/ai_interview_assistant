"""
Subscription Service - [АЗ + ДОБРО]
Управление подписками
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from app.models.subscription import Subscription, SubscriptionTier, SubscriptionStatus
from app.models.payment import Payment, PaymentStatus


class SubscriptionService:
    """Сервис управления подписками"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def activate_subscription(
        self,
        user_id: str,
        tier: SubscriptionTier,
        period: str,  # "monthly" или "yearly"
        operation_id: str
    ) -> Subscription:
        """
        Активировать подписку после успешной оплаты
        
        Args:
            user_id: ID пользователя
            tier: Тарифный план
            period: Период подписки
            operation_id: ID операции из Банка Точка
        
        Returns:
            Обновленная подписка
        """
        # Получаем или создаем подписку
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        if not subscription:
            subscription = Subscription(user_id=user_id)
            self.db.add(subscription)
        
        # Обновляем подписку
        subscription.tier = tier
        subscription.status = SubscriptionStatus.ACTIVE
        subscription.tochka_operation_id = operation_id
        subscription.current_period_start = datetime.utcnow()
        
        # Устанавливаем дату окончания
        if period == "yearly":
            subscription.current_period_end = datetime.utcnow() + timedelta(days=365)
        else:  # monthly
            subscription.current_period_end = datetime.utcnow() + timedelta(days=30)
        
        self.db.commit()
        self.db.refresh(subscription)
        
        return subscription
    
    def cancel_subscription(self, user_id: str, immediately: bool = False) -> Subscription:
        """
        Отменить подписку
        
        Args:
            user_id: ID пользователя
            immediately: Отменить немедленно или в конце периода
        
        Returns:
            Обновленная подписка
        """
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()
        
        if not subscription:
            raise ValueError("Подписка не найдена")
        
        if immediately:
            subscription.status = SubscriptionStatus.CANCELED
            subscription.tier = SubscriptionTier.FREE
            subscription.current_period_end = datetime.utcnow()
        else:
            subscription.cancel_at_period_end = True
        
        subscription.canceled_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(subscription)
        
        return subscription
    
    def get_subscription(self, user_id: str) -> Optional[Subscription]:
        """Получить подписку пользователя"""
        return self.db.query(Subscription).filter(
            Subscription.user_id == user_id
        ).first()

