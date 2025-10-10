# 🏗️ Архитектура Hintsage

## Онтология "Ясна" - Функция = Архетип

Весь проект построен на принципе **"Функция в коде = Архетип"**.

### Таблица соответствий модулей архетипам:

| Модуль | Архетипы | Функции | Технологии |
|--------|----------|---------|-----------|
| **config_manager** | ДОБРО + АЗ | Управление настройками, хранение секретов | YAML, cryptography |
| **llm_integration** | РЦИ + ИЖЕ | Запросы к OpenAI API | openai-python |
| **context_manager** | ПАМЯТЬ + ДОБРО | История диалога, сериализация | JSON, datetime |
| **audio_capture** | ВЕДИ + ИЖЕ | Захват аудиопотока | sounddevice, numpy |
| **stt** | МЫСЛЕТЕ + ВЕДИ | Распознавание речи | Vosk, Whisper |
| **question_detector** | ЧЕЛО + МЫСЛЕТЕ | Детекция вопросов | regex, transformers |
| **ui_overlay** | ЛИЧЬ + ЧЕЛО | Графический интерфейс | PyQt6 |
| **security** | ШТОР + ТАЙНА | Антидетект, защита | WinAPI, ctypes |
| **screenshot_ocr** | ВЕДИ + МЫСЛЕТЕ | Скриншоты, OCR | PIL, EasyOCR/Tesseract |
| **teleprompter** | ЛИЧЬ + СЛОВО | Телесуфлёр | PyQt6 |
| **syntax_highlighter** | МЫСЛЕТЕ + ЛИЧЬ | Подсветка кода | Pygments, Markdown |

## Диаграмма потока данных

```
┌──────────────┐
│  Микрофон    │
└──────┬───────┘
       │
       ▼
┌──────────────────┐     ┌──────────────┐
│  Audio Capture   │────▶│  STT Engine  │
│  [ВЕДИ + ИЖЕ]    │     │ [МЫСЛЕТЕ +   │
└──────────────────┘     │     ВЕДИ]    │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │   Question   │
                         │   Detector   │
                         │ [ЧЕЛО +      │
                         │  МЫСЛЕТЕ]    │
                         └──────┬───────┘
                                │
                   ┌────────────┴────────────┐
                   │ Вопрос обнаружен?      │
                   └────────────┬────────────┘
                                │ Да
                                ▼
                         ┌──────────────┐
                         │   Context    │
                         │   Manager    │
                         │ [ПАМЯТЬ +    │
                         │    ДОБРО]    │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │     LLM      │
                         │  Integration │
                         │  [РЦИ + ИЖЕ] │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │   Syntax     │
                         │ Highlighter  │
                         │ [МЫСЛЕТЕ +   │
                         │    ЛИЧЬ]     │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ UI Overlay   │
                         │ [ЛИЧЬ + ЧЕЛО]│
                         └──────────────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  Пользователь│
                         └──────────────┘
```

## Модульная структура

```
hintsage/
├── modules/
│   ├── config_manager/        # [ДОБРО + АЗ]
│   │   ├── __init__.py
│   │   └── config_manager.py
│   │       ├── load_config()          # Загрузить конфигурацию
│   │       ├── save_config()          # Сохранить конфигурацию
│   │       ├── encrypt_api_key()      # Шифрование ключа
│   │       └── validate_config()      # Валидация
│   │
│   ├── llm_integration/       # [РЦИ + ИЖЕ]
│   │   ├── __init__.py
│   │   └── llm_client.py
│   │       ├── generate_response()    # Генерация ответа
│   │       ├── validate_api_key()     # Проверка ключа
│   │       └── change_model()         # Смена модели
│   │
│   ├── context_manager/       # [ПАМЯТЬ + ДОБРО]
│   │   ├── __init__.py
│   │   └── context_manager.py
│   │       ├── add_message()          # Добавить сообщение
│   │       ├── get_context()          # Получить контекст
│   │       ├── save_session()         # Сохранить сессию
│   │       └── export_to_markdown()   # Экспорт
│   │
│   ├── audio_capture/         # [ВЕДИ + ИЖЕ]
│   │   ├── __init__.py
│   │   └── audio_capture.py
│   │       ├── start()                # Начать захват
│   │       ├── stop()                 # Остановить
│   │       ├── get_audio_chunk()      # Получить чанк
│   │       └── get_buffer()           # Получить буфер
│   │
│   ├── stt/                   # [МЫСЛЕТЕ + ВЕДИ]
│   │   ├── __init__.py
│   │   └── stt_engine.py
│   │       ├── VoskSTT                # Vosk движок
│   │       ├── WhisperSTT             # Whisper движок
│   │       └── STTManager             # Менеджер
│   │
│   ├── question_detector/     # [ЧЕЛО + МЫСЛЕТЕ]
│   │   ├── __init__.py
│   │   └── question_detector.py
│   │       ├── is_question()          # Проверка вопроса
│   │       ├── should_trigger()       # Должен ли триггер
│   │       └── analyze_text()         # Анализ текста
│   │
│   ├── ui_overlay/            # [ЛИЧЬ + ЧЕЛО]
│   │   ├── __init__.py
│   │   └── overlay_window.py
│   │       ├── display_answer()       # Показать ответ
│   │       ├── set_status()           # Установить статус
│   │       └── toggle_phantom_mode()  # Фантом режим
│   │
│   ├── security/              # [ШТОР + ТАЙНА]
│   │   ├── __init__.py
│   │   └── security_manager.py
│   │       ├── apply_window_protection()  # Защита окна
│   │       ├── enable_click_through()     # Click-through
│   │       └── check_screen_capture_active() # Детект захвата
│   │
│   ├── screenshot_ocr/        # [ВЕДИ + МЫСЛЕТЕ]
│   │   ├── __init__.py
│   │   └── screenshot_manager.py
│   │       ├── capture_screen()       # Захват
│   │       ├── ocr_image()            # OCR
│   │       └── capture_and_ocr()      # Захват + OCR
│   │
│   ├── teleprompter/          # [ЛИЧЬ + СЛОВО]
│   │   ├── __init__.py
│   │   └── teleprompter.py
│   │       ├── set_text()             # Установить текст
│   │       ├── start_scroll()         # Начать прокрутку
│   │       └── stop_scroll()          # Остановить
│   │
│   └── syntax_highlighter/    # [МЫСЛЕТЕ + ЛИЧЬ]
│       ├── __init__.py
│       └── highlighter.py
│           ├── highlight_code()       # Подсветка кода
│           ├── process_markdown()     # Обработка Markdown
│           └── format_answer()        # Форматирование ответа
│
├── main.py                    # Главное приложение
├── config.yaml                # Конфигурация
├── requirements.txt           # Зависимости
└── README.md                  # Документация
```

## Потоки и асинхронность

### Основной поток (Main Thread):
- UI (PyQt6 event loop)
- Управление компонентами
- Обработка сигналов

### Поток обработки аудио (AudioProcessingThread):
- Непрерывный захват аудио
- STT транскрипция
- Отправка распознанного текста в главный поток

### Асинхронные операции:
- LLM запросы (можно сделать async)
- OCR обработка
- Сохранение истории

## Принципы проектирования

### 1. Разделение ответственности (ДОБРО + ОТ)
Каждый модуль отвечает за одну функцию:
- `audio_capture` - только захват аудио
- `stt` - только распознавание
- `llm_integration` - только общение с LLM

### 2. Слабая связанность (ЛАДЪ + ДОБРО)
Модули общаются через четкие интерфейсы:
- Сигналы PyQt6
- Функции с четкими контрактами
- Минимум зависимостей

### 3. Конфигурируемость (ВЕДИ + ДОБРО)
Все настройки в `config.yaml`:
- Выбор движков (Vosk/Whisper)
- Параметры моделей
- UI настройки

### 4. Безопасность (ШТОР + ТАЙНА)
- Шифрование API ключей
- Антидетект функции
- Локальное хранение данных

## Расширяемость

### Добавление нового STT движка:

```python
# modules/stt/stt_engine.py

class CustomSTT(STTEngine):
    def transcribe(self, audio_data, sample_rate):
        # Ваша реализация
        pass
    
    def is_ready(self):
        return True

# В STTManager:
self.engines["custom"] = CustomSTT()
```

### Добавление нового LLM провайдера:

```python
# modules/llm_integration/providers/anthropic_client.py

class AnthropicClient:
    def generate_response(self, question, context):
        # Интеграция с Claude
        pass
```

### Добавление новых детекторов вопросов:

```python
# В question_detector.py:
def add_pattern(self, pattern: str):
    self.patterns.append(pattern)
```

## Метрики и мониторинг

### Логирование (ВЕДИ + СЛОВО):
- `loguru` для структурированных логов
- Ротация по дням
- Разные уровни (DEBUG, INFO, ERROR)

### Статистика (ВЕДИ + МЫСЛЕТЕ):
```python
stats = context_manager.get_statistics()
# {
#   "total_messages": 20,
#   "user_messages": 10,
#   "assistant_messages": 10,
#   "avg_answer_length": 450
# }
```

## Безопасность и приватность

### Данные не покидают компьютер:
- ✅ Аудио - обрабатывается локально
- ✅ История - хранится локально
- ✅ API ключ - шифруется локально
- ❌ LLM запросы - идут в OpenAI (это неизбежно)

### Антидетект:
- Windows API для невидимости окна
- Исключение из захвата экрана
- Phantom mode для мыши
- Скрытие из панели задач

## Оптимизация производительности

### Узкие места (НАВЬ):
1. **STT транскрипция** - используйте Vosk для скорости
2. **LLM генерация** - кэшируйте частые вопросы
3. **OCR обработка** - делайте в отдельном потоке

### Решения (ЛАДЪ + ПУТЬ):
```python
# Кэширование LLM ответов
@lru_cache(maxsize=128)
def get_cached_answer(question):
    return llm_client.generate_response(question)
```

---

**Архитектура построена на онтологии "Ясна" - каждая функция соответствует архетипу, что обеспечивает ясность и модульность кода.**


