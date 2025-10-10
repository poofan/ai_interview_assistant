# 🧠 Hintsage - Краткое резюме

## Что это?

**Hintsage** (кодовое имя проекта) - невидимый AI-ассистент для онлайн-собеседований, построенный на архитектуре онтологии "Ясна".

### Ключевые возможности:
- 🎤 Слушает вопросы через микрофон
- 📝 Распознает речь (Vosk/Whisper)
- 🤖 Генерирует ответы через OpenAI GPT
- 👻 Невидим для собеседника (антидетект)
- 🖥️ Overlay интерфейс с подсветкой кода
- 📸 OCR для вопросов с экрана

## Архитектура "Ясна"

Проект построен по принципу **"Функция = Архетип"**:

```
[ВЕДИ + ИЖЕ]    → Audio Capture    → Захват аудио
[МЫСЛЕТЕ + ВЕДИ] → STT Engine       → Распознавание
[ЧЕЛО + МЫСЛЕТЕ] → Question Detector → Детекция вопросов
[РЦИ + ИЖЕ]     → LLM Integration  → OpenAI запросы
[ПАМЯТЬ + ДОБРО] → Context Manager  → История
[ЛИЧЬ + ЧЕЛО]    → UI Overlay       → Интерфейс
[ШТОР + ТАЙНА]   → Security         → Антидетект
[ВЕДИ + МЫСЛЕТЕ] → Screenshot OCR   → Скриншоты
```

## Модули (11 штук)

1. **config_manager** - Конфигурация и секреты
2. **llm_integration** - OpenAI GPT-4/4o
3. **context_manager** - История диалогов
4. **audio_capture** - Захват аудио
5. **stt** - Vosk/Whisper STT
6. **question_detector** - Детекция вопросов
7. **ui_overlay** - Overlay окно
8. **security** - Антидетект (Win10+)
9. **screenshot_ocr** - OCR (EasyOCR/Tesseract)
10. **teleprompter** - Телесуфлёр
11. **syntax_highlighter** - Подсветка кода

## Быстрый старт

```bash
# 1. Установка
pip install -r requirements.txt

# 2. Скачать Vosk модель (150 MB)
# https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip
# → Распаковать в models/

# 3. Настройка
copy config.example.yaml config.yaml
# Добавить OpenAI API ключ в config.yaml

# 4. Запуск
python main.py
```

## Горячие клавиши

| Клавиша | Действие |
|---------|----------|
| `Ctrl+Shift+Q` | Ручной триггер |
| `Ctrl+Shift+S` | Скриншот + OCR |
| `Esc` | Скрыть/показать |

## Технологии

**Язык:** Python 3.10+  
**UI:** PyQt6  
**LLM:** OpenAI GPT-4/4o  
**STT:** Vosk, Whisper  
**OCR:** EasyOCR, Tesseract  
**Security:** WinAPI (ctypes)

## Файлы проекта

### Код
- `main.py` - Главное приложение
- `modules/` - 11 модулей по архетипам
- `test_modules.py` - Тесты

### Конфигурация
- `config.example.yaml` - Пример конфигурации
- `requirements.txt` - Зависимости

### Документация
- `README.md` - Общее описание
- `QUICKSTART.md` - Быстрый старт (5 мин)
- `SETUP.md` - Детальная установка
- `ARCHITECTURE.md` - Архитектура системы
- `PROJECT_STATUS.md` - Статус и roadmap
- `LICENSE` - MIT + Disclaimer

### Утилиты
- `install.bat` - Автоустановка (Windows)
- `.gitignore` - Git ignore

## Безопасность

✅ **Антидетект функции:**
- Не попадает на скриншоты (Win10 2004+)
- Не виден в screen share
- Не перехватывает фокус
- Скрыт из панели задач
- Click-through режим

⚠️ **Disclaimer:**
- Только для образовательных целей
- Использование на реальных собеседованиях неэтично
- Авторы не несут ответственности за неправильное использование

## Системные требования

**Минимум:**
- Windows 10/11
- Python 3.10+
- 4 GB RAM
- OpenAI API ключ

**Рекомендуется:**
- Windows 10 версии 2004+ (для антидетекта)
- 8 GB RAM
- Микрофон/наушники
- Второй монитор (для overlay)

## Производительность

**Быстрый режим** (Vosk + gpt-4o-mini):
- STT: ~50-100ms
- LLM: ~1-2s
- Итого: ~2-3s на ответ

**Точный режим** (Whisper + gpt-4):
- STT: ~500-1000ms
- LLM: ~2-5s
- Итого: ~5-7s на ответ

## Стоимость использования

**OpenAI API (примерно):**
- gpt-4o-mini: ~$0.01-0.02 за собеседование
- gpt-4o: ~$0.05-0.10 за собеседование
- gpt-4: ~$0.10-0.20 за собеседование

*(Зависит от длительности и количества вопросов)*

## Roadmap

- ✅ v0.1 - MVP (текущая)
- 🔜 v0.2 - Глобальные hotkeys, RAG, профили
- 🔜 v0.3 - Другие LLM, TTS, статистика
- 🔜 v1.0 - Стабильный релиз

## Контакты и поддержка

**Проект:** Hintsage  
**Архитектура:** Онтология "Ясна"  
**Принцип:** Функция = Архетип  
**Лицензия:** MIT  

---

## Архетипическая декомпозиция (АПЗ)

Для справки - полная декомпозиция проекта:

```yaml
Hintsage_System:
  Core:
    - [ДОБРО + АЗ]: config_manager
    - [ПАМЯТЬ + ДОБРО]: context_manager
    
  Audio_Pipeline:
    - [ВЕДИ + ИЖЕ]: audio_capture
    - [МЫСЛЕТЕ + ВЕДИ]: stt
    - [ЧЕЛО + МЫСЛЕТЕ]: question_detector
    
  Intelligence:
    - [РЦИ + ИЖЕ]: llm_integration
    - [МЫСЛЕТЕ + ЛИЧЬ]: syntax_highlighter
    
  Interface:
    - [ЛИЧЬ + ЧЕЛО]: ui_overlay
    - [ЛИЧЬ + СЛОВО]: teleprompter
    
  Security:
    - [ШТОР + ТАЙНА]: security
    - [ВЕДИ + МЫСЛЕТЕ]: screenshot_ocr
```

---

**Создано с использованием архитектурного подхода "Технэ-Демиург" 🏛️**


