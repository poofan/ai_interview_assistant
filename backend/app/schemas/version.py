"""
Version Schemas - [АЗ + ДОБРО]
Pydantic модели для проверки версий
"""

from pydantic import BaseModel
from typing import List, Optional


class VersionCheckRequest(BaseModel):
    """Запрос на проверку версии"""
    current_version: str
    platform: str = "windows"


class VersionCheckResponse(BaseModel):
    """Ответ с информацией о версии"""
    latest_version: str
    update_available: bool
    critical: bool = False
    changelog: Optional[List[str]] = None
    download_url: Optional[str] = None
    min_version: Optional[str] = None

