"""
Payments API Endpoints - [АЗ + ДОБРО]
Эндпоинты для работы с платежами (Банк Точка)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.payment import PaymentCreateRequest, PaymentResponse
from app.models.user import User
from app.models.subscription import SubscriptionTier
from app.middleware.auth import get_current_active_user
from app.services.payment_service import PaymentService
from app.services.subscription_service import SubscriptionService
from datetime import datetime

router = APIRouter()


@router.post("/create", response_model=PaymentResponse)
async def create_payment(
    request: PaymentCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Создать платеж в Банке Точка
    
    - **tier**: Тарифный план ("pro" или "enterprise")
    - **period**: Период подписки ("monthly" или "yearly")
    
    Returns:
        Ссылка на оплату и данные платежа
    """
    payment_service = PaymentService(db)
    
    # Валидация tier
    tier_map = {"pro": SubscriptionTier.PRO, "enterprise": SubscriptionTier.ENTERPRISE}
    if request.tier not in tier_map:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный тарифный план. Допустимые: pro, enterprise"
        )
    
    # Валидация period
    if request.period not in ["monthly", "yearly"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный период. Допустимые: monthly, yearly"
        )
    
    try:
        payment_data = await payment_service.create_payment(
            user_id=str(current_user.id),
            tier=tier_map[request.tier],
            period=request.period,
            user_email=current_user.email,
            user_name=current_user.name
        )
        
        return PaymentResponse(**payment_data, status="CREATED")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка создания платежа: {str(e)}"
        )


@router.get("/{operation_id}", response_model=dict)
async def get_payment_status(
    operation_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Получить статус платежа
    
    Args:
        operation_id: ID операции из Банка Точка
    
    Returns:
        Статус платежа
    """
    payment_service = PaymentService(db)
    
    try:
        payment_data = await payment_service.get_payment_status(operation_id)
        
        if not payment_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Платеж не найден"
            )
        
        return payment_data
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения статуса: {str(e)}"
        )


@router.post("/webhooks/tochka")
async def tochka_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Webhook от Банка Точка для уведомлений о статусе платежа
    
    Этот эндпоинт вызывается Банком Точка когда статус платежа меняется
    """
    try:
        # Получаем данные из webhook
        payload = await request.json()
        
        operation_data = payload.get("Data", {}).get("Operation", [])
        if not operation_data:
            return {"status": "ignored", "reason": "no_operation_data"}
        
        operation = operation_data[0] if isinstance(operation_data, list) else operation_data
        
        operation_id = operation.get("operationId")
        status_value = operation.get("status")
        paid_at_str = operation.get("paidAt")
        
        if not operation_id or not status_value:
            return {"status": "ignored", "reason": "missing_required_fields"}
        
        # Обновляем статус платежа в БД
        payment_service = PaymentService(db)
        
        paid_at = None
        if paid_at_str and status_value == "PAID":
            try:
                paid_at = datetime.fromisoformat(paid_at_str.replace("Z", "+00:00"))
            except:
                paid_at = datetime.utcnow()
        
        payment_service.update_payment_status(operation_id, status_value, paid_at)
        
        # Если платеж оплачен - активируем подписку
        if status_value == "PAID":
            from app.models.payment import Payment
            payment = db.query(Payment).filter(
                Payment.tochka_operation_id == operation_id
            ).first()
            
            if payment:
                subscription_service = SubscriptionService(db)
                
                tier_map = {"pro": SubscriptionTier.PRO, "enterprise": SubscriptionTier.ENTERPRISE}
                tier = tier_map.get(payment.subscription_tier, SubscriptionTier.PRO)
                
                subscription_service.activate_subscription(
                    user_id=str(payment.user_id),
                    tier=tier,
                    period=payment.subscription_period,
                    operation_id=operation_id
                )
        
        return {
            "status": "success",
            "operation_id": operation_id,
            "new_status": status_value
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

