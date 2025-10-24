"""
Teleprompter - [ЛИЧЬ + СЛОВО]
Мини-окно для удобного чтения ответов
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from loguru import logger


class TeleprompterWindow(QWidget):
    """
    Окно телесуфлёра
    Архетипы:
    - ЛИЧЬ: визуальное представление
    - СЛОВО: отображение текста
    - ЛАДЪ: удобочитаемость
    """
    
    def __init__(
        self,
        width: int = 300,
        height: int = 200,
        font_size: int = 16,
        font_family: str = "Consolas",
        scroll_speed: int = 50
    ):
        """
        Инициализация телесуфлёра
        
        Args:
            width: Ширина окна
            height: Высота окна
            font_size: Размер шрифта
            font_family: Семейство шрифта
            scroll_speed: Скорость прокрутки (мс)
        """
        super().__init__()
        
        self.window_width = width
        self.window_height = height
        self.font_size = font_size
        self.font_family = font_family
        self.scroll_speed = scroll_speed
        
        self.current_text = ""
        self.current_position = 0
        
        self._setup_window()
        self._setup_ui()
        
        # Таймер для автопрокрутки
        self.scroll_timer = QTimer()
        self.scroll_timer.timeout.connect(self._auto_scroll)
        
        logger.info(f"[OK] TeleprompterWindow создано ({width}x{height})")
    
    def _setup_window(self) -> None:
        """
        [ЛИЧЬ] - Настройка окна
        """
        self.setWindowTitle("Hintsage Teleprompter")
        self.setGeometry(100, 100, self.window_width, self.window_height)
        
        # Always on top, frameless
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        
        # Прозрачность
        self.setWindowOpacity(0.9)
    
    def _setup_ui(self) -> None:
        """
        [ЛИЧЬ + СЛОВО] - Настройка UI
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Текстовая метка
        self.text_label = QLabel("")
        self.text_label.setFont(QFont(self.font_family, self.font_size))
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        layout.addWidget(self.text_label)
        
        # Темная тема
        self._apply_theme()
    
    def _apply_theme(self) -> None:
        """
        [ЛИЧЬ] - Применить тему
        """
        style = """
        QWidget {
            background-color: #000000;
        }
        QLabel {
            color: #00ff00;
            padding: 5px;
        }
        """
        self.setStyleSheet(style)
    
    def set_text(self, text: str) -> None:
        """
        [СЛОВО] - Установить текст
        
        Args:
            text: Текст для отображения
        """
        self.current_text = text
        self.current_position = 0
        self._update_display()
    
    def start_scroll(self) -> None:
        """
        [ИЖЕ + СЛОВО] - Запустить автопрокрутку
        """
        self.scroll_timer.start(self.scroll_speed)
        logger.debug("Автопрокрутка запущена")
    
    def stop_scroll(self) -> None:
        """
        [НАВЬ] - Остановить автопрокрутку
        """
        self.scroll_timer.stop()
        logger.debug("Автопрокрутка остановлена")
    
    def _auto_scroll(self) -> None:
        """
        [ИЖЕ] - Автоматическая прокрутка
        """
        if self.current_position < len(self.current_text):
            self.current_position += 1
            self._update_display()
        else:
            self.stop_scroll()
    
    def _update_display(self) -> None:
        """
        [ЛИЧЬ] - Обновить отображение
        """
        # Показываем часть текста
        visible_text = self.current_text[:self.current_position]
        self.text_label.setText(visible_text)
    
    def set_font_size(self, size: int) -> None:
        """
        [ЛИЧЬ] - Изменить размер шрифта
        
        Args:
            size: Новый размер
        """
        self.font_size = size
        self.text_label.setFont(QFont(self.font_family, self.font_size))
    
    def keyPressEvent(self, event):
        """Горячие клавиши"""
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        elif event.key() == Qt.Key.Key_Space:
            # Пробел - пауза/возобновление
            if self.scroll_timer.isActive():
                self.stop_scroll()
            else:
                self.start_scroll()


