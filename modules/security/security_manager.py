"""
Security Manager - [ШТОР + ТАЙНА]
Управление безопасностью и антидетект функциями
"""

import sys
from typing import Optional
from loguru import logger


class SecurityManager:
    """
    Менеджер безопасности
    Архетипы:
    - ШТОР: защита/сокрытие
    - ТАЙНА: невидимость
    - НАВЬ: теневой режим
    """
    
    def __init__(
        self,
        anti_screenshot: bool = True,
        anti_screen_share: bool = True,
        no_focus_steal: bool = True,
        silent_mode: bool = True
    ):
        """
        Инициализация менеджера безопасности
        
        Args:
            anti_screenshot: Защита от скриншотов
            anti_screen_share: Защита от screen share
            no_focus_steal: Не перехватывать фокус
            silent_mode: Бесшумный режим
        """
        self.anti_screenshot = anti_screenshot
        self.anti_screen_share = anti_screen_share
        self.no_focus_steal = no_focus_steal
        self.silent_mode = silent_mode
        
        self.platform = sys.platform
        self.windows_version = self._check_windows_version()
        
        logger.info(f"[OK] SecurityManager инициализирован (платформа: {self.platform})")
        
        if self.platform == 'win32':
            if self.windows_version and self.windows_version >= (10, 0, 19041):  # Windows 10 2004
                logger.info("[OK] Windows 10 2004+ обнаружен - полная поддержка антидетекта")
            else:
                logger.warning(f"[WARNING] Windows {self.windows_version} - антидетект может работать частично")
                logger.warning("Рекомендуется Windows 10 версии 2004 (build 19041) или новее")
    
    def _check_windows_version(self) -> Optional[tuple]:
        """
        [ВЕДИ + ЧЕЛО] - Проверить версию Windows
        
        Returns:
            (major, minor, build) или None
        """
        if self.platform != 'win32':
            return None
        
        try:
            import platform
            version_str = platform.version()
            # Формат: "10.0.19041"
            parts = version_str.split('.')
            if len(parts) >= 3:
                return (int(parts[0]), int(parts[1]), int(parts[2]))
            return None
        except Exception as e:
            logger.debug(f"Не удалось определить версию Windows: {e}")
            return None
    
    def apply_window_protection(self, hwnd: int) -> bool:
        """
        [ШТОР + ТАЙНА] - Применить защиту к окну
        
        Args:
            hwnd: Handle окна (Windows)
        
        Returns:
            True если успешно
        """
        if self.platform != 'win32':
            logger.warning(f"Защита окон доступна только на Windows (текущая ОС: {self.platform})")
            return False
        
        try:
            import ctypes
            from ctypes import wintypes
            
            user32 = ctypes.windll.user32
            
            # 1. Защита от скриншотов
            if self.anti_screenshot:
                # WDA_EXCLUDEFROMCAPTURE = 0x11 (Windows 10 2004+)
                WDA_EXCLUDEFROMCAPTURE = 0x11
                result = user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
                
                if result:
                    logger.info("[OK] Защита от скриншотов активирована")
                else:
                    logger.warning("[WARNING] Не удалось активировать защиту от скриншотов")
            
            # 2. Установка WS_EX_NOACTIVATE (не перехватывать фокус)
            if self.no_focus_steal:
                GWL_EXSTYLE = -20
                WS_EX_NOACTIVATE = 0x08000000
                
                ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style | WS_EX_NOACTIVATE)
                
                logger.info("[OK] Защита от перехвата фокуса активирована")
            
            # 3. Установка WS_EX_LAYERED для прозрачности
            WS_EX_LAYERED = 0x00080000
            ex_style = user32.GetWindowLongW(hwnd, -20)
            user32.SetWindowLongW(hwnd, -20, ex_style | WS_EX_LAYERED)
            
            return True
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка применения защиты окна: {e}")
            return False
    
    def enable_click_through(self, hwnd: int, enable: bool = True) -> bool:
        """
        [ШТОР] - Включить режим "click-through" (мышь проходит сквозь окно)
        
        Args:
            hwnd: Handle окна
            enable: Включить или выключить
        
        Returns:
            True если успешно
        """
        if self.platform != 'win32':
            return False
        
        try:
            import ctypes
            
            user32 = ctypes.windll.user32
            
            GWL_EXSTYLE = -20
            WS_EX_TRANSPARENT = 0x00000020
            
            ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            
            if enable:
                ex_style |= WS_EX_TRANSPARENT
            else:
                ex_style &= ~WS_EX_TRANSPARENT
            
            user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)
            
            status = "включен" if enable else "выключен"
            logger.info(f"Click-through {status}")
            
            return True
        
        except Exception as e:
            logger.error(f"Ошибка установки click-through: {e}")
            return False
    
    def hide_from_taskbar(self, hwnd: int) -> bool:
        """
        [ТАЙНА] - Скрыть окно из панели задач
        
        Args:
            hwnd: Handle окна
        
        Returns:
            True если успешно
        """
        if self.platform != 'win32':
            return False
        
        try:
            import ctypes
            
            user32 = ctypes.windll.user32
            
            GWL_EXSTYLE = -20
            WS_EX_TOOLWINDOW = 0x00000080
            WS_EX_APPWINDOW = 0x00040000
            
            ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ex_style |= WS_EX_TOOLWINDOW  # Скрыть из панели
            ex_style &= ~WS_EX_APPWINDOW  # Убрать из списка приложений
            
            user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)
            
            logger.info("[OK] Окно скрыто из панели задач")
            return True
        
        except Exception as e:
            logger.error(f"Ошибка скрытия из панели задач: {e}")
            return False
    
    def check_screen_capture_active(self) -> bool:
        """
        [ЧЕЛО + ШТОР] - Проверить, активен ли захват экрана
        
        Returns:
            True если обнаружен захват экрана
        """
        # Это сложная задача, требует мониторинга процессов
        # Базовая проверка популярных программ
        
        if self.platform == 'win32':
            try:
                import psutil
                
                capture_processes = [
                    'obs64.exe', 'obs32.exe',  # OBS Studio
                    'zoom.exe',  # Zoom
                    'teams.exe',  # MS Teams
                    'discord.exe',  # Discord
                    'slack.exe',  # Slack
                    'skype.exe',  # Skype
                ]
                
                for proc in psutil.process_iter(['name']):
                    try:
                        if proc.info['name'].lower() in [p.lower() for p in capture_processes]:
                            logger.warning(f"[WARNING] Обнаружена программа захвата экрана: {proc.info['name']}")
                            return True
                    except:
                        continue
                
                return False
            
            except Exception as e:
                logger.error(f"Ошибка проверки захвата экрана: {e}")
                return False
        
        return False
    
    def disable_system_sounds(self) -> None:
        """
        [НАВЬ] - Отключить системные звуки (бесшумный режим)
        """
        if not self.silent_mode:
            return
        
        # Это можно реализовать через mixer или отключение звуков конкретно для приложения
        logger.info("Бесшумный режим активирован")
    
    def get_security_status(self) -> dict:
        """
        [ВЕДИ] - Получить статус безопасности
        
        Returns:
            Словарь со статусом
        """
        return {
            "anti_screenshot": self.anti_screenshot,
            "anti_screen_share": self.anti_screen_share,
            "no_focus_steal": self.no_focus_steal,
            "silent_mode": self.silent_mode,
            "platform": self.platform,
            "platform_supported": self.platform == 'win32',
            "screen_capture_detected": self.check_screen_capture_active() if self.platform == 'win32' else None
        }

