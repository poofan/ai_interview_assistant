"""
Screenshot Manager - [ВЕДИ + МЫСЛЕТЕ]
Захват скриншотов и OCR
"""

from PIL import ImageGrab, Image
import numpy as np
from typing import Optional, Tuple, List
from pathlib import Path
from datetime import datetime
from loguru import logger
import io


class ScreenshotManager:
    """
    Менеджер скриншотов и OCR
    Архетипы:
    - ВЕДИ: захват изображения
    - МЫСЛЕТЕ: распознавание текста
    - ПАМЯТЬ: сохранение
    """
    
    def __init__(
        self,
        ocr_engine: str = "easyocr",
        languages: List[str] = None,
        save_screenshots: bool = False,
        screenshot_path: str = "data/screenshots",
        gpu: bool = False
    ):
        """
        Инициализация менеджера скриншотов
        
        Args:
            ocr_engine: Движок OCR (tesseract, easyocr)
            languages: Языки для OCR
            save_screenshots: Сохранять ли скриншоты
            screenshot_path: Путь для сохранения
            gpu: Использовать GPU для OCR
        """
        self.ocr_engine = ocr_engine
        self.languages = languages or ["ru", "en"]
        self.save_screenshots = save_screenshots
        self.screenshot_path = Path(screenshot_path)
        self.gpu = gpu
        
        self.ocr_reader = None
        
        # Создаем директорию
        if self.save_screenshots:
            self.screenshot_path.mkdir(parents=True, exist_ok=True)
        
        self._init_ocr()
        
        logger.info(f"[OK] ScreenshotManager инициализирован (OCR: {ocr_engine})")
    
    def _init_ocr(self) -> None:
        """
        [ВЕДИ + МЫСЛЕТЕ] - Инициализировать OCR движок
        """
        try:
            if self.ocr_engine == "easyocr":
                import easyocr
                
                gpu_status = "GPU" if self.gpu else "CPU"
                logger.info(f"Загрузка EasyOCR (языки: {self.languages}, устройство: {gpu_status})...")
                self.ocr_reader = easyocr.Reader(self.languages, gpu=self.gpu)
                logger.info(f"[OK] EasyOCR загружен ({gpu_status})")
            
            elif self.ocr_engine == "tesseract":
                import pytesseract
                
                # Проверяем наличие tesseract
                try:
                    pytesseract.get_tesseract_version()
                    self.ocr_reader = pytesseract
                    logger.info("[OK] Tesseract OCR доступен")
                except Exception as e:
                    logger.error(f"Tesseract не найден: {e}")
                    logger.warning("Установите Tesseract OCR: https://github.com/tesseract-ocr/tesseract")
            
            else:
                logger.error(f"Неизвестный OCR движок: {self.ocr_engine}")
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка инициализации OCR: {e}")
    
    def capture_screen(self, bbox: Optional[Tuple[int, int, int, int]] = None) -> Optional[Image.Image]:
        """
        [ВЕДИ] - Захватить скриншот
        
        Args:
            bbox: Координаты области (x1, y1, x2, y2) или None для полного экрана
        
        Returns:
            PIL Image или None
        """
        try:
            screenshot = ImageGrab.grab(bbox=bbox)
            
            logger.debug(f"Скриншот захвачен: {screenshot.size}")
            
            # Сохраняем если нужно
            if self.save_screenshots:
                self._save_screenshot(screenshot)
            
            return screenshot
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка захвата скриншота: {e}")
            return None
    
    def capture_region_interactive(self) -> Optional[Image.Image]:
        """
        [ВЕДИ + ЧЕЛО] - Интерактивный захват региона
        (упрощенная версия - полный экран, можно расширить до выбора области)
        
        Returns:
            PIL Image или None
        """
        logger.info("Захват области... (для интерактивного выбора нужна дополнительная реализация)")
        return self.capture_screen()
    
    def ocr_image(self, image: Image.Image) -> str:
        """
        [МЫСЛЕТЕ] - Распознать текст на изображении
        
        Args:
            image: PIL Image
        
        Returns:
            Распознанный текст
        """
        if not self.ocr_reader:
            logger.error("OCR движок не инициализирован")
            return ""
        
        try:
            if self.ocr_engine == "easyocr":
                # Конвертируем PIL -> numpy
                img_array = np.array(image)
                
                results = self.ocr_reader.readtext(img_array)
                
                # Извлекаем текст
                text = " ".join([result[1] for result in results])
                
                logger.info(f"[OK] EasyOCR распознал {len(results)} текстовых блоков")
                
                return text
            
            elif self.ocr_engine == "tesseract":
                # Формируем язык для tesseract
                lang = "+".join(self.languages)
                
                text = self.ocr_reader.image_to_string(image, lang=lang)
                
                logger.info(f"[OK] Tesseract распознал текст ({len(text)} символов)")
                
                return text.strip()
            
            else:
                logger.error("OCR движок не поддерживается")
                return ""
        
        except Exception as e:
            logger.error(f"[ERROR] Ошибка OCR: {e}")
            return ""
    
    def capture_and_ocr(self, bbox: Optional[Tuple[int, int, int, int]] = None) -> str:
        """
        [ВЕДИ + МЫСЛЕТЕ] - Захватить и распознать
        
        Args:
            bbox: Координаты области
        
        Returns:
            Распознанный текст
        """
        screenshot = self.capture_screen(bbox)
        
        if screenshot:
            return self.ocr_image(screenshot)
        
        return ""
    
    def _save_screenshot(self, image: Image.Image) -> str:
        """
        [ПАМЯТЬ] - Сохранить скриншот
        
        Args:
            image: PIL Image
        
        Returns:
            Путь к сохраненному файлу
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = self.screenshot_path / filename
        
        try:
            image.save(filepath)
            logger.debug(f"Скриншот сохранен: {filepath}")
            return str(filepath)
        
        except Exception as e:
            logger.error(f"Ошибка сохранения скриншота: {e}")
            return ""
    
    def stitch_screenshots(self, images: List[Image.Image], direction: str = "vertical") -> Optional[Image.Image]:
        """
        [МЫСЛЕТЕ + ВЕДИ] - Склеить несколько скриншотов
        
        Args:
            images: Список изображений
            direction: Направление (vertical, horizontal)
        
        Returns:
            Склеенное изображение
        """
        if not images:
            return None
        
        try:
            if direction == "vertical":
                # Вертикальная склейка
                total_height = sum(img.height for img in images)
                max_width = max(img.width for img in images)
                
                result = Image.new('RGB', (max_width, total_height))
                
                y_offset = 0
                for img in images:
                    result.paste(img, (0, y_offset))
                    y_offset += img.height
            
            else:  # horizontal
                total_width = sum(img.width for img in images)
                max_height = max(img.height for img in images)
                
                result = Image.new('RGB', (total_width, max_height))
                
                x_offset = 0
                for img in images:
                    result.paste(img, (x_offset, 0))
                    x_offset += img.width
            
            logger.info(f"[OK] Склеено {len(images)} изображений ({direction})")
            return result
        
        except Exception as e:
            logger.error(f"Ошибка склейки изображений: {e}")
            return None


