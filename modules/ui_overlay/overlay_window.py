"""
Overlay Window - [ЛИЧЬ + ЧЕЛО]
Невидимый overlay интерфейс с антидетект функциями
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QFont, QPalette, QColor
from loguru import logger
import sys


class OverlayWindow(QMainWindow):
    """
    Overlay окно для отображения ответов
    Архетипы:
    - ЛИЧЬ: интерфейс
    - ЧЕЛО: взаимодействие
    - ШТОР: невидимость/защита
    """
    
    # Сигналы
    trigger_question = pyqtSignal()
    clear_context = pyqtSignal()
    take_screenshot = pyqtSignal()
    
    def __init__(
        self,
        width: int = 400,
        height: int = 600,
        position: str = "top-right",
        opacity: float = 0.95,
        phantom_mode: bool = True,
        anti_screenshot: bool = True
    ):
        """
        Инициализация overlay окна
        
        Args:
            width: Ширина окна
            height: Высота окна
            position: Позиция (top-left, top-right, bottom-left, bottom-right)
            opacity: Прозрачность (0-1)
            phantom_mode: Режим фантома (мышь проходит сквозь)
            anti_screenshot: Защита от скриншотов
        """
        super().__init__()
        
        self.window_width = width
        self.window_height = height
        self.position_mode = position
        self.opacity_value = opacity
        self.phantom_mode = phantom_mode
        self.anti_screenshot = anti_screenshot
        
        self._setup_window()
        self._setup_ui()
        self._apply_anti_detection()
        
        logger.info(f"[OK] OverlayWindow создано ({width}x{height}, {position})")
    
    def _setup_window(self) -> None:
        """
        [ЛИЧЬ + ШТОР] - Настройка окна
        """
        # Базовые настройки
        self.setWindowTitle("Hintsage")
        self.setGeometry(0, 0, self.window_width, self.window_height)
        
        # Always on top
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool  # Не показывается в панели задач
        )
        
        # Прозрачность
        self.setWindowOpacity(self.opacity_value)
        
        # Позиция на экране
        self._set_position()
    
    def _setup_ui(self) -> None:
        """
        [ЛИЧЬ + ЧЕЛО] - Настройка интерфейса
        """
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Заголовок
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("[HINTSAGE] Hintsage")
        self.title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        # Кнопка минимизации
        self.minimize_btn = QPushButton("_")
        self.minimize_btn.setMaximumWidth(30)
        self.minimize_btn.clicked.connect(self.hide)
        header_layout.addWidget(self.minimize_btn)
        
        # Кнопка закрытия
        self.close_btn = QPushButton("×")
        self.close_btn.setMaximumWidth(30)
        self.close_btn.clicked.connect(self.close)
        header_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(header_layout)
        
        # Статус
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Готов к работе")
        self.status_label.setStyleSheet("color: #00ff00; font-size: 10px;")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        # [TIER] - Индикатор тарифа
        self.tier_label = QLabel("🎯 FREE")
        self.tier_label.setStyleSheet("color: #888888; font-size: 9px; font-weight: bold;")
        self.tier_label.setToolTip("Текущий тариф подписки")
        status_layout.addWidget(self.tier_label)
        
        # [ПАМЯТЬ] - Индикатор контекста
        self.context_label = QLabel("📝 Контекст: 0")
        self.context_label.setStyleSheet("color: #ffaa00; font-size: 9px;")
        self.context_label.setToolTip("Количество сообщений в памяти")
        status_layout.addWidget(self.context_label)
        
        main_layout.addLayout(status_layout)
        
        # Область отображения ответа
        self.answer_display = QTextEdit()
        self.answer_display.setReadOnly(True)
        self.answer_display.setFont(QFont("Consolas", 11))
        self.answer_display.setPlaceholderText("Ответы будут отображаться здесь...")
        main_layout.addWidget(self.answer_display, stretch=1)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.trigger_btn = QPushButton("[TRIGGER] Триггер (Ctrl+Shift+Q)")
        self.trigger_btn.clicked.connect(self.trigger_question.emit)
        buttons_layout.addWidget(self.trigger_btn)
        
        self.screenshot_btn = QPushButton("[SCREENSHOT] Скрин")
        self.screenshot_btn.clicked.connect(self.take_screenshot.emit)
        buttons_layout.addWidget(self.screenshot_btn)
        
        self.clear_btn = QPushButton("[CLEAR] Очистить")
        self.clear_btn.clicked.connect(self._clear_display)
        buttons_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # Применяем темную тему
        self._apply_dark_theme()
    
    def _apply_dark_theme(self) -> None:
        """
        [ЛИЧЬ] - Применить темную тему
        """
        dark_style = """
        QMainWindow {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        QTextEdit {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton {
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #555555;
            border-radius: 3px;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #4c4c4c;
        }
        QPushButton:pressed {
            background-color: #2c2c2c;
        }
        QLabel {
            color: #ffffff;
        }
        """
        self.setStyleSheet(dark_style)
    
    def _apply_anti_detection(self) -> None:
        """
        [ШТОР + ТАЙНА] - Применить защиту от детекции
        """
        # Phantom mode - мышь проходит сквозь окно
        if self.phantom_mode:
            self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)  # Изначально False
        
        # Защита от скриншотов (Windows)
        if self.anti_screenshot and sys.platform == 'win32':
            try:
                import ctypes
                from ctypes import wintypes
                
                hwnd = int(self.winId())
                
                # WDA_EXCLUDEFROMCAPTURE = 0x11
                # Исключает окно из захвата (Windows 10 2004+)
                WDA_EXCLUDEFROMCAPTURE = 0x11
                
                user32 = ctypes.windll.user32
                user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
                
                logger.info("[OK] Антискриншот защита активирована")
            
            except Exception as e:
                logger.warning(f"Не удалось активировать антискриншот: {e}")
    
    def _set_position(self) -> None:
        """
        [ДОБРО] - Установить позицию окна
        """
        from PyQt6.QtWidgets import QApplication
        
        screen = QApplication.primaryScreen().geometry()
        
        if self.position_mode == "top-left":
            x, y = 0, 0
        elif self.position_mode == "top-right":
            x = screen.width() - self.window_width
            y = 0
        elif self.position_mode == "bottom-left":
            x = 0
            y = screen.height() - self.window_height
        elif self.position_mode == "bottom-right":
            x = screen.width() - self.window_width
            y = screen.height() - self.window_height
        else:
            x = screen.width() - self.window_width
            y = 0
        
        self.move(x, y)
    
    def display_answer(self, answer: str, append_mode: bool = True) -> None:
        """
        [ЛИЧЬ + СЛОВО] - Отобразить ответ
        
        Args:
            answer: Текст ответа
            append_mode: True = добавлять к существующему, False = перезаписать
        """
        if append_mode:
            # [ПАМЯТЬ + СЛОВО] - Накопительный режим
            current_text = self.answer_display.toPlainText()
            
            if current_text:
                # Добавляем разделитель между ответами
                separator = "\n\n" + "─" * 60 + "\n\n"
                new_text = current_text + separator + answer
            else:
                new_text = answer
            
            self.answer_display.setPlainText(new_text)
            
            # Прокрутка вниз
            scrollbar = self.answer_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        else:
            # Режим перезаписи
            self.answer_display.setPlainText(answer)
        
        self.status_label.setText("[OK] Ответ получен")
        self.status_label.setStyleSheet("color: #00ff00;")
        
        logger.debug(f"Отображен ответ ({len(answer)} символов, append={append_mode})")
    
    def append_answer(self, text: str) -> None:
        """
        [ЛИЧЬ + ИЖЕ] - Добавить текст к ответу (для потоковой генерации)
        
        Args:
            text: Текст для добавления
        """
        self.answer_display.insertPlainText(text)
        # Прокрутка вниз
        scrollbar = self.answer_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def _clear_display(self) -> None:
        """
        [ПАМЯТЬ] - Очистить отображение
        """
        self.answer_display.clear()
        self.status_label.setText("Очищено")
        self.clear_context.emit()
    
    def set_status(self, status: str, color: str = "#ffffff") -> None:
        """
        [ЛИЧЬ] - Установить статус
        
        Args:
            status: Текст статуса
            color: Цвет текста (hex)
        """
        self.status_label.setText(status)
        self.status_label.setStyleSheet(f"color: {color}; font-size: 10px;")
    
    def update_context_indicator(self, message_count: int) -> None:
        """
        [ПАМЯТЬ + ЛИЧЬ] - Обновить индикатор контекста
        
        Args:
            message_count: Количество сообщений в контексте
        """
        self.context_label.setText(f"📝 Контекст: {message_count}")
        
        # Меняем цвет в зависимости от заполненности
        if message_count == 0:
            color = "#666666"  # Серый
        elif message_count < 10:
            color = "#00ff00"  # Зеленый
        elif message_count < 20:
            color = "#ffaa00"  # Оранжевый
        else:
            color = "#ff6600"  # Красный (близко к лимиту)
        
        self.context_label.setStyleSheet(f"color: {color}; font-size: 9px;")
    
    def update_tier_indicator(self, tier: str) -> None:
        """
        [TIER] - Обновить индикатор тарифа
        
        Args:
            tier: Название тарифа (FREE, PRO, ENTERPRISE)
        """
        tier_upper = tier.upper()
        
        # Цвета для разных тарифов
        tier_colors = {
            "FREE": "#888888",      # Серый
            "PRO": "#00aaff",       # Синий
            "ENTERPRISE": "#ff9900"  # Оранжевый
        }
        
        # Эмодзи для разных тарифов
        tier_emojis = {
            "FREE": "🆓",
            "PRO": "⭐",
            "ENTERPRISE": "💎"
        }
        
        color = tier_colors.get(tier_upper, "#888888")
        emoji = tier_emojis.get(tier_upper, "🎯")
        
        self.tier_label.setText(f"{emoji} {tier_upper}")
        self.tier_label.setStyleSheet(f"color: {color}; font-size: 9px; font-weight: bold;")
        self.tier_label.setToolTip(f"Текущий тариф: {tier_upper}")
        
        logger.info(f"[TIER] Индикатор обновлен: {tier_upper}")
    
    def show_loading(self) -> None:
        """
        [ЛИЧЬ] - Показать индикатор загрузки
        """
        self.set_status("[WAIT] Генерация ответа...", "#ffaa00")
    
    def show_error(self, error: str) -> None:
        """
        [ЛИЧЬ + НАВЬ] - Показать ошибку
        
        Args:
            error: Текст ошибки
        """
        self.set_status(f"[ERROR] {error}", "#ff0000")
        self.answer_display.setPlainText(f"Ошибка: {error}")
    
    def toggle_phantom_mode(self) -> None:
        """
        [ШТОР] - Переключить режим фантома
        """
        self.phantom_mode = not self.phantom_mode
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, self.phantom_mode)
        
        status = "включен" if self.phantom_mode else "выключен"
        logger.info(f"Phantom mode {status}")
    
    def set_opacity(self, opacity: float) -> None:
        """
        [ЛИЧЬ] - Установить прозрачность
        
        Args:
            opacity: Прозрачность (0-1)
        """
        self.opacity_value = max(0.1, min(1.0, opacity))
        self.setWindowOpacity(self.opacity_value)
    
    def move_to_corner(self, corner: str) -> None:
        """
        [ДОБРО + ЛИЧЬ] - Переместить окно в угол
        
        Args:
            corner: Угол (top-left, top-right, bottom-left, bottom-right)
        """
        self.position_mode = corner
        self._set_position()
        logger.info(f"Окно перемещено: {corner}")
    
    def snap_to_safe_position(self) -> None:
        """
        [ЛАДЪ + ЛИЧЬ] - Переместить в безопасную позицию (не перекрывает активное окно)
        """
        from PyQt6.QtWidgets import QApplication
        
        # Получаем все экраны
        screens = QApplication.screens()
        
        if len(screens) > 1:
            # Если есть второй монитор - используем его
            second_screen = screens[1].geometry()
            x = second_screen.x() + second_screen.width() - self.window_width
            y = second_screen.y()
            self.move(x, y)
            logger.info("Окно перемещено на второй монитор")
        else:
            # Иначе в угол основного экрана
            self._set_position()
    
    def minimize_to_corner(self) -> None:
        """
        [ЛИЧЬ] - Свернуть в маленький значок в углу
        """
        # Сохраняем текущий размер
        self.normal_size = (self.window_width, self.window_height)
        
        # Уменьшаем до минимума (только заголовок)
        self.resize(100, 40)
        logger.debug("Окно свернуто в минирежим")
    
    def toggle_window(self) -> None:
        """
        [ЧЕЛО + ЛИЧЬ] - Переключить видимость окна
        Глобальная горячая клавиша для сворачивания/разворачивания
        """
        if self.isVisible():
            self.hide()
            logger.debug("[TOGGLE] Окно скрыто")
        else:
            self.show()
            self.activateWindow()
            self.raise_()
            logger.debug("[TOGGLE] Окно показано")
    
    def keyPressEvent(self, event):
        """
        Обработка горячих клавиш
        """
        # Esc - скрыть окно
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        
        # Ctrl+Q - закрыть
        elif event.key() == Qt.Key.Key_Q and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.close()
    
    def mousePressEvent(self, event):
        """
        Обработка перетаскивания окна
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """
        Перетаскивание окна
        """
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

