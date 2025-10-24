#!/usr/bin/env python3
"""
Тест OCR функциональности
"""

import sys
import traceback
from pathlib import Path

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent))

def test_easyocr():
    """Тест EasyOCR"""
    print("Тестируем EasyOCR...")
    
    try:
        import easyocr
        print("EasyOCR импортирован успешно")
        
        # Пробуем инициализировать
        print("Инициализируем EasyOCR...")
        reader = easyocr.Reader(['ru', 'en'], gpu=False)  # CPU для теста
        print("EasyOCR инициализирован успешно")
        
        # Тест с простым изображением
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np
        
        # Создаем тестовое изображение с текстом
        img = Image.new('RGB', (300, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        # Пробуем нарисовать текст
        try:
            draw.text((10, 30), "Test OCR", fill='black')
            print("Тестовое изображение создано")
            
            # Конвертируем в numpy
            img_array = np.array(img)
            print("Изображение конвертировано в numpy")
            
            # Пробуем распознать
            results = reader.readtext(img_array)
            print(f"EasyOCR распознал {len(results)} блоков текста")
            
            if results:
                text = " ".join([result[1] for result in results])
                print(f"Распознанный текст: '{text}'")
            else:
                print("Текст не распознан")
                
        except Exception as e:
            print(f"Ошибка при тестировании: {e}")
            traceback.print_exc()
            
    except ImportError as e:
        print(f"EasyOCR не найден: {e}")
        return False
    except Exception as e:
        print(f"Ошибка инициализации EasyOCR: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_tesseract():
    """Тест Tesseract"""
    print("\nТестируем Tesseract...")
    
    try:
        import pytesseract
        print("pytesseract импортирован успешно")
        
        # Проверяем версию
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract версия: {version}")
        
        return True
        
    except ImportError as e:
        print(f"pytesseract не найден: {e}")
        return False
    except Exception as e:
        print(f"Ошибка Tesseract: {e}")
        return False

def test_screenshot():
    """Тест захвата скриншота"""
    print("\nТестируем захват скриншота...")
    
    try:
        from PIL import ImageGrab
        screenshot = ImageGrab.grab()
        print(f"Скриншот захвачен: {screenshot.size}")
        
        # Сохраняем для проверки
        screenshot.save("test_screenshot.png")
        print("Скриншот сохранен как test_screenshot.png")
        
        return True
        
    except Exception as e:
        print(f"Ошибка захвата скриншота: {e}")
        return False

if __name__ == "__main__":
    print("Тестирование OCR компонентов...\n")
    
    # Тестируем все компоненты
    easyocr_ok = test_easyocr()
    tesseract_ok = test_tesseract()
    screenshot_ok = test_screenshot()
    
    print(f"\nРезультаты:")
    print(f"EasyOCR: {'OK' if easyocr_ok else 'FAIL'}")
    print(f"Tesseract: {'OK' if tesseract_ok else 'FAIL'}")
    print(f"Screenshot: {'OK' if screenshot_ok else 'FAIL'}")
    
    if easyocr_ok and screenshot_ok:
        print("\nOCR должен работать!")
    else:
        print("\nЕсть проблемы с OCR")
