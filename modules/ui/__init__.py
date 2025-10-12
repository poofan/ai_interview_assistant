"""
UI Components - [ДОБРО + АЗ]
Компоненты пользовательского интерфейса
"""

from .error_handler import ErrorHandler, get_error_handler, handle_api_error
from .update_dialog import UpdateDialog, show_update_dialog

__all__ = [
    "ErrorHandler",
    "get_error_handler",
    "handle_api_error",
    "UpdateDialog",
    "show_update_dialog",
]

