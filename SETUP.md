# 🚀 Инструкция по установке Hintsage

## Шаг 1: Подготовка окружения

### Windows 10/11

```bash
# 1. Установите Python 3.10+ (если еще не установлен)
# Скачайте с https://www.python.org/downloads/

# 2. Клонируйте репозиторий (или распакуйте архив)
cd C:\git\ai_interview_assistant

# 3. Создайте виртуальное окружение
python -m venv venv

# 4. Активируйте окружение
venv\Scripts\activate

# 5. Обновите pip
python -m pip install --upgrade pip
```

## Шаг 2: Установка зависимостей

```bash
# Установите все зависимости
pip install -r requirements.txt
```

### Важные зависимости:

#### Tesseract OCR (опционально, если используете tesseract):
1. Скачайте установщик: https://github.com/UB-Mannheim/tesseract/wiki
2. Установите Tesseract
3. Добавьте в PATH: `C:\Program Files\Tesseract-OCR\tesseract.exe`

#### PyAudio (если возникают проблемы):
```bash
# Скачайте wheel для Windows
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
pip install PyAudio-0.2.13-cp310-cp310-win_amd64.whl
```

## Шаг 3: Загрузка моделей STT

### Vosk (рекомендуется для быстрой работы):

```bash
# Создайте папку для моделей
mkdir models

# Скачайте русскую модель Vosk (150 MB):
# https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip

# Распакуйте в папку models/
# Должно получиться: models/vosk-model-small-ru-0.22/
```

### Whisper (опционально):
Whisper загружается автоматически при первом запуске.

## Шаг 4: Настройка конфигурации

```bash
# 1. Скопируйте пример конфигурации
copy config.example.yaml config.yaml

# 2. Откройте config.yaml в текстовом редакторе
notepad config.yaml
```

### Обязательные настройки:

1. **OpenAI API ключ**:
   ```yaml
   openai:
     api_key: "sk-ваш-ключ-здесь"
   ```
   
   Получить ключ: https://platform.openai.com/api-keys

2. **Выбор STT движка**:
   ```yaml
   stt:
     default_engine: "vosk"  # или "whisper"
     language: "ru"
   ```

3. **Путь к модели Vosk** (если используете):
   ```yaml
   stt:
     vosk:
       model_path: "models/vosk-model-small-ru-0.22"
   ```

## Шаг 5: Первый запуск

```bash
# Убедитесь, что виртуальное окружение активно
# (в начале строки должно быть (venv))

python main.py
```

### Ожидаемый вывод:
```
============================================================
🧠 Hintsage - AI Interview Assistant
Архитектура: Онтология 'Ясна'
============================================================
✅ ConfigManager инициализирован
✅ LLM Client инициализирован (модель: gpt-4o)
✅ ContextManager инициализирован
✅ AudioCapture инициализирован
✅ Vosk модель загружена
✅ QuestionDetector инициализирован
✅ OverlayWindow создано
✅ SecurityManager инициализирован
✅ ScreenshotManager инициализирован
🚀 Запуск Hintsage...
✅ Hintsage запущен!
```

## Шаг 6: Проверка работы

1. **Overlay окно** должно появиться в правом верхнем углу
2. **Говорите в микрофон** - текст должен распознаваться
3. **Задайте вопрос**: "Как работает binary search?"
4. **Дождитесь ответа** от GPT

### Горячие клавиши:
- `Ctrl+Shift+Q` - Ручной триггер (захват последних 10 секунд аудио)
- `Ctrl+Shift+S` - Сделать скриншот и распознать текст
- `Esc` - Скрыть/показать overlay
- Кнопка `×` - Закрыть приложение

## Шаг 7: Настройка антидетекта (Windows 10 2004+)

Антидетект функции требуют:
- Windows 10 версии 2004 или новее
- Права администратора (для некоторых функций)

Проверка версии Windows:
```cmd
winver
```

### Функции антидетекта:
- ✅ Не попадает на скриншоты (Windows 10 2004+)
- ✅ Не виден в screen share Zoom/Teams
- ✅ Не перехватывает фокус
- ✅ Скрыт из панели задач

## Возможные проблемы

### 1. "Vosk модель не найдена"
```bash
# Проверьте путь к модели в config.yaml
# Убедитесь, что папка models/vosk-model-small-ru-0.22/ существует
```

### 2. "OpenAI API ключ неверный"
```bash
# Проверьте ключ в config.yaml
# Убедитесь, что у вас есть кредиты на аккаунте OpenAI
# https://platform.openai.com/account/billing
```

### 3. "Микрофон не работает"
```python
# Добавьте в main.py перед запуском:
audio_capture.list_devices()
# Выберите нужное устройство
```

### 4. "OCR не работает"
```bash
# Если используете EasyOCR, первый запуск загружает модели (~100 MB)
# Дождитесь загрузки

# Или переключитесь на Tesseract в config.yaml:
screenshot:
  ocr_engine: "tesseract"
```

### 5. "Антидетект не работает"
```
# Убедитесь, что у вас Windows 10 2004+
# Запустите от имени администратора
```

## Оптимизация производительности

### Для слабых ПК:
```yaml
# В config.yaml:

# Используйте Vosk вместо Whisper
stt:
  default_engine: "vosk"

# Используйте меньшую модель GPT
openai:
  model: "gpt-4o-mini"

# Отключите ML детекцию вопросов
question_detector:
  mode: "regex"  # вместо "hybrid"
```

### Для мощных ПК:
```yaml
# Используйте Whisper
stt:
  default_engine: "whisper"
  whisper:
    model_size: "medium"  # или "large"
    device: "cuda"  # если есть NVIDIA GPU

# Включите ML детекцию
question_detector:
  mode: "hybrid"
```

## Безопасность

1. **Никогда не коммитьте** `config.yaml` с API ключом
2. **Используйте шифрование**:
   ```yaml
   security:
     encrypt_api_key: true
   ```
3. **Очищайте историю** после собеседований:
   ```bash
   del data\sessions\*.json
   ```

## Тестирование

```bash
# Запустите без микрофона (тестовый режим)
python main.py --test

# Проверьте все модули
python -m pytest tests/
```

## Следующие шаги

1. Настройте системный промпт под свой профиль в `config.yaml`
2. Добавьте свои regex паттерны для детекции вопросов
3. Настройте позицию и прозрачность overlay окна
4. Протестируйте на тестовом собеседовании!

---

**Удачи на собеседованиях! 🚀**


