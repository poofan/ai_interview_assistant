"""
Payment Service - [АЗ + ДОБРО]
Интеграция с Банком Точка для обработки платежей
"""

import httpx
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.payment import Payment, PaymentStatus
from app.models.subscription import SubscriptionTier

settings = get_settings()


class PaymentService:
    """
    Сервис работы с платежами через Банк Точка
    Архетипы: АЗ (управление транзакциями) + ДОБРО (финансовые операции)
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.api_url = f"{settings.TOCHKA_API_URL}/acquiring/v1.0"
        self.headers = {
            "Authorization": f"Bearer {settings.TOCHKA_BEARER_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def create_payment(
        self,
        user_id: str,
        tier: SubscriptionTier,
        period: str,  # "monthly" или "yearly"
        user_email: str,
        user_name: Optional[str] = None,
        user_phone: Optional[str] = None
    ) -> Dict:
        """
        Создать платеж в Банке Точка
        
        Args:
            user_id: ID пользователя
            tier: Тарифный план
            period: Период подписки
            user_email: Email пользователя
            user_name: Имя пользователя
            user_phone: Телефон пользователя
        
        Returns:
            Данные платежа с payment_link
        """
        # Определяем сумму
        amount = self._get_price(tier, period)
        
        # Формируем назначение платежа
        tier_names = {
            SubscriptionTier.PRO: "Pro",
            SubscriptionTier.ENTERPRISE: "Enterprise"
        }
        period_names = {"monthly": "месяц", "yearly": "год"}
        
        purpose = f"Подписка Hintsage {tier_names.get(tier, 'Pro')} на {period_names.get(period, 'месяц')}"
        
        # Подготавливаем данные для API
        payload = {
            "Data": {
                "customerCode": settings.TOCHKA_CUSTOMER_CODE,
                "amount": f"{amount:.2f}",
                "purpose": purpose,
                "redirectUrl": f"{settings.FRONTEND_URL}/payment/success",
                "failRedirectUrl": f"{settings.FRONTEND_URL}/payment/failed",
                "paymentMode": ["sbp", "card", "tinkoff"],
                "merchantId": settings.TOCHKA_MERCHANT_ID,
                "taxSystemCode": settings.TOCHKA_TAX_SYSTEM_CODE,
                "Client": {
                    "name": user_name or user_email,
                    "email": user_email,
                    "phone": user_phone or "+79999999999"  # Заглушка если нет телефона
                },
                "Items": [
                    {
                        "vatType": "none",
                        "name": purpose,
                        "amount": f"{amount:.2f}",
                        "quantity": 1,
                        "paymentMethod": "full_payment",
                        "paymentObject": "service",
                        "measure": "шт."
                    }
                ]
            }
        }
        
        # Отправляем запрос в Банк Точка
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/payments_with_receipt",
                json=payload,
                headers=self.headers,
                timeout=30.0
            )
            
            response.raise_for_status()
            result = response.json()
        
        # Сохраняем платеж в БД
        operation_id = result["Data"]["operationId"]
        payment_link = result["Data"]["paymentLink"]
        
        payment = Payment(
            user_id=user_id,
            tochka_operation_id=operation_id,
            amount=amount,
            purpose=purpose,
            status=PaymentStatus.CREATED,
            payment_link=payment_link,
            payment_mode=result["Data"].get("paymentMode", []),
            subscription_tier=tier.value,
            subscription_period=period,
            client_name=user_name,
            client_email=user_email,
            client_phone=user_phone,
            tochka_raw_data=result
        )
        
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        
        return {
            "operation_id": operation_id,
            "payment_link": payment_link,
            "amount": amount,
            "purpose": purpose
        }
    
    async def get_payment_status(self, operation_id: str) -> Optional[Dict]:
        """
        Получить статус платежа из Банка Точка
        
        Args:
            operation_id: ID операции
        
        Returns:
            Информация о платеже
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/payments/{operation_id}",
                headers=self.headers,
                timeout=10.0
            )
            
            if response.status_code == 200:
                return response.json()
            return None
    
    def update_payment_status(self, operation_id: str, status: str, paid_at: Optional[datetime] = None):
        """
        Обновить статус платежа в БД
        
        Args:
            operation_id: ID операции
            status: Новый статус
            paid_at: Дата оплаты
        """
        payment = self.db.query(Payment).filter(
            Payment.tochka_operation_id == operation_id
        ).first()
        
        if payment:
            payment.status = PaymentStatus[status]
            if paid_at:
                payment.paid_at = paid_at
            
            self.db.commit()
    
    def _get_price(self, tier: SubscriptionTier, period: str) -> float:
        """
        Получить цену подписки
        
        Args:
            tier: Тарифный план
            period: Период
        
        Returns:
            Цена в рублях
        """
        prices = {
            (SubscriptionTier.PRO, "monthly"): settings.PRICE_PRO_MONTHLY,
            (SubscriptionTier.PRO, "yearly"): settings.PRICE_PRO_YEARLY,
            (SubscriptionTier.ENTERPRISE, "monthly"): settings.PRICE_ENTERPRISE_MONTHLY,
            (SubscriptionTier.ENTERPRISE, "yearly"): settings.PRICE_ENTERPRISE_YEARLY,
        }
        
        return prices.get((tier, period), settings.PRICE_PRO_MONTHLY)

