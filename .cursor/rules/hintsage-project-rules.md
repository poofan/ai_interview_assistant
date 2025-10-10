# Правила разработки проекта Hintsage

## Архитектурные принципы

### 1. Онтология "Ясна" - Функция = Архетип

Каждый новый модуль/функция должна соответствовать архетипу:

```python
# Правильно:
def capture_audio():  # [ВЕДИ + ИЖЕ]
    """Захват аудиопотока"""
    pass

def transcribe_speech():  # [МЫСЛЕТЕ + ВЕДИ]
    """Преобразование речи в текст"""
    pass

# Неправильно:
def do_everything():  # ❌ Слишком много ответственности
    pass
```

### 2. Модульность

- Каждый модуль отвечает за ОДНУ функцию
- Слабая связанность между модулями
- Четкие интерфейсы

### 3. Конфигурируемость

- ВСЕ настройки в `config.yaml`
- Нет хардкода
- Валидация при запуске

## Структура нового модуля

```
modules/
└── new_module/              # [АРХЕТИП1 + АРХЕТИП2]
    ├── __init__.py         # Экспорт основного класса
    └── new_module.py       # Реализация
```

**Шаблон модуля:**

```python
"""
New Module - [АРХЕТИП1 + АРХЕТИП2]
Описание функциональности
"""

from loguru import logger

class NewModule:
    """
    Описание модуля
    Архетипы:
    - АРХЕТИП1: функция1
    - АРХЕТИП2: функция2
    """
    
    def __init__(self, config_param: str):
        """Инициализация"""
        self.config_param = config_param
        logger.info(f"✅ NewModule инициализирован")
    
    def main_function(self):
        """[АРХЕТИП] - Основная функция"""
        pass
```

## Логирование

**Используйте loguru:**

```python
from loguru import logger

# Уровни:
logger.debug("Отладочная информация")
logger.info("✅ Успешная операция")
logger.warning("⚠️ Предупреждение")
logger.error("❌ Ошибка")
```

**Стиль сообщений:**
- ✅ "ConfigManager инициализирован"
- 🎤 "Захват аудио запущен"
- 📝 "Распознано: текст"
- 🔔 "Триггер вопроса!"
- ⏳ "Генерация ответа..."
- ❌ "Ошибка: описание"

## Обработка ошибок

```python
try:
    # Операция
    pass
except SpecificError as e:
    logger.error(f"❌ Конкретная ошибка: {e}")
    # Fallback или raise
except Exception as e:
    logger.error(f"❌ Неожиданная ошибка: {e}")
    raise
```

## Документация

### Docstrings:

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    [АРХЕТИП] - Краткое описание
    
    Args:
        param1: Описание параметра
        param2: Описание параметра
    
    Returns:
        Описание возвращаемого значения
    """
    pass
```

### Комментарии к архетипам:

```python
# [ВЕДИ + ИЖЕ] - Захват данных
def capture_data():
    pass

# [МЫСЛЕТЕ] - Обработка
def process_data():
    pass

# [ПАМЯТЬ + ДОБРО] - Сохранение
def save_data():
    pass
```

## Добавление зависимостей

1. Добавьте в `requirements.txt`
2. Укажите версию: `package>=version`
3. Добавьте комментарий о назначении:

```txt
# Core
python>=3.10

# STT
vosk>=0.3.45  # Быстрый оффлайн STT
```

## Конфигурация

При добавлении новых настроек:

1. Добавьте в `config.example.yaml`
2. Добавьте комментарий
3. Укажите значение по умолчанию

```yaml
# New Feature [АРХЕТИП]
new_feature:
  enabled: true
  parameter: "default_value"  # Описание параметра
```

## Тестирование

При добавлении нового модуля:

1. Добавьте тест в `test_modules.py`
2. Проверьте импорт
3. Проверьте основную функциональность

```python
def test_new_module():
    """Тест нового модуля"""
    logger.info("\n=== Тест: NewModule ===")
    
    try:
        from modules.new_module import NewModule
        
        module = NewModule(config_param="test")
        # Тесты
        
        logger.info("✅ NewModule работает")
    
    except Exception as e:
        logger.error(f"❌ NewModule: {e}")
```

## Git Workflow

### Коммиты:

```bash
# Формат:
[АРХЕТИП] Краткое описание

# Примеры:
git commit -m "[ВЕДИ + ИЖЕ] Добавлен модуль audio_capture"
git commit -m "[ЛИЧЬ] Улучшен UI overlay окна"
git commit -m "[ТАЙНА + ШТОР] Усилена защита от скриншотов"
```

### Ветки:

```bash
feature/module-name    # Новая функциональность
fix/issue-description  # Исправление бага
refactor/module-name   # Рефакторинг
docs/topic             # Документация
```

## Безопасность

### Запрещено:

- ❌ Коммитить `config.yaml` с реальными ключами
- ❌ Хранить API ключи в коде
- ❌ Логировать чувствительные данные

### Обязательно:

- ✅ Шифровать секреты
- ✅ Использовать `.gitignore`
- ✅ Валидировать входные данные

## Производительность

### Оптимизация:

```python
# Асинхронность для I/O
async def async_function():
    pass

# Кэширование
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function():
    pass

# Ленивая загрузка
def lazy_load():
    if not hasattr(self, '_cached_data'):
        self._cached_data = load_heavy_data()
    return self._cached_data
```

## UI Guidelines

### Стиль сообщений:

- ✅ Успех: зеленый `#00ff00`
- ⏳ Загрузка: оранжевый `#ffaa00`
- ❌ Ошибка: красный `#ff0000`
- ℹ️ Инфо: белый `#ffffff`

### Темная тема:

```python
dark_style = """
QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
}
"""
```

## Архетипы - Справка

| Архетип | Функция | Примеры |
|---------|---------|---------|
| ВЕДИ | Получение данных | capture, fetch, read |
| МЫСЛЕТЕ | Обработка | transform, process, analyze |
| ДОБРО | Организация | manage, configure, validate |
| ПАМЯТЬ | Хранение | save, load, cache |
| РЦИ | Внешние запросы | request, call, query |
| ИЖЕ | Передача/поток | stream, send, transfer |
| ЧЕЛО | Распознавание | detect, recognize, identify |
| ЛИЧЬ | Интерфейс | display, show, render |
| ШТОР | Защита | protect, secure, guard |
| ТАЙНА | Сокрытие | hide, encrypt, conceal |
| СЛОВО | Текст/вывод | log, write, export |
| АЗ | Учетные данные | authenticate, authorize |
| ЛАДЪ | Оптимизация | optimize, improve, balance |
| НАВЬ | Теневой режим | silent, background, invisible |

## Чек-лист перед коммитом

- [ ] Код следует архетипическому принципу
- [ ] Добавлены логи (loguru)
- [ ] Обработаны ошибки
- [ ] Добавлены docstrings
- [ ] Обновлен `config.example.yaml` (если нужно)
- [ ] Добавлены тесты в `test_modules.py`
- [ ] Обновлена документация (если нужно)
- [ ] Нет хардкода
- [ ] Нет секретов в коде

---

**Помни: Функция = Архетип. Каждый модуль - это воплощение архетипа "Ясна".**


