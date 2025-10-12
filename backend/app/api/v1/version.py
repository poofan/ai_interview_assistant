"""
Version API Endpoints - [АЗ + ДОБРО]
Эндпоинты для проверки версий приложения
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from packaging import version as pkg_version

from app.database import get_db
from app.schemas.version import VersionCheckRequest, VersionCheckResponse
from app.models.app_version import AppVersion
from app.config import get_settings

settings = get_settings()
router = APIRouter()


@router.post("/check", response_model=VersionCheckResponse)
async def check_version(
    request: VersionCheckRequest,
    db: Session = Depends(get_db)
):
    """
    Проверить наличие обновлений приложения
    
    - **current_version**: Текущая версия приложения (например, "1.0.0")
    - **platform**: Платформа ("windows", "macos", "linux")
    
    Returns:
        Информация о последней версии и доступных обновлениях
    """
    # Получаем последнюю версию из БД
    latest_version_record = db.query(AppVersion).filter(
        AppVersion.platform == request.platform,
        AppVersion.active == True
    ).order_by(AppVersion.release_date.desc()).first()
    
    # Если нет записей в БД, используем конфигурацию
    if not latest_version_record:
        return VersionCheckResponse(
            latest_version=settings.LATEST_APP_VERSION,
            update_available=False,
            critical=False,
            download_url=settings.APP_DOWNLOAD_URL
        )
    
    # Сравниваем версии
    try:
        current = pkg_version.parse(request.current_version)
        latest = pkg_version.parse(latest_version_record.version)
        update_available = latest > current
    except:
        update_available = False
    
    # Парсим changelog (если это JSON array)
    changelog = None
    if latest_version_record.changelog:
        try:
            import json
            changelog = json.loads(latest_version_record.changelog)
            if not isinstance(changelog, list):
                changelog = [latest_version_record.changelog]
        except:
            changelog = [latest_version_record.changelog]
    
    return VersionCheckResponse(
        latest_version=latest_version_record.version,
        update_available=update_available,
        critical=latest_version_record.critical,
        changelog=changelog,
        download_url=latest_version_record.download_url,
        min_version=latest_version_record.min_version
    )

