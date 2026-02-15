"""
Users API Endpoints - [АЗ + ДОБРО]
Эндпоинты для работы с пользователями
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.subscription import SubscriptionResponse
from app.models.user import User
from app.models.subscription import Subscription
from app.middleware.auth import get_current_active_user
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Получить информацию о текущем пользователе
    
    Requires:
        JWT token в заголовке Authorization: Bearer <token>
    
    Returns:
        Данные текущего пользователя
    """
    return UserResponse.from_orm(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Обновить профиль текущего пользователя
    
    - **name**: Новое имя (опционально)
    - **avatar_url**: URL аватара (опционально)
    
    Returns:
        Обновленные данные пользователя
    """
    user_service = UserService(db)
    
    # Обновляем только переданные поля
    update_data = user_update.dict(exclude_unset=True)
    updated_user = user_service.update_user(current_user, **update_data)
    
    return UserResponse.from_orm(updated_user)


@router.get("/me/subscription", response_model=SubscriptionResponse)
async def get_current_user_subscription(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Получить информацию о подписке текущего пользователя
    
    Returns:
        Данные подписки (tier, features, status)
    """
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()
    
    if not subscription:
        # Если подписки нет, возвращаем FREE
        subscription = Subscription(
            user_id=current_user.id,
            tier="free",
            status="active"
        )
    
    return SubscriptionResponse(
        id=str(subscription.id),
        tier=subscription.tier.value,
        status=subscription.status.value,
        features=subscription.features,
        current_period_start=subscription.current_period_start,
        current_period_end=subscription.current_period_end,
        is_active=subscription.is_active
    )

