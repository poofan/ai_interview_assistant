# 🗄️ Database Setup Guide

## 📋 **Требования:**

- PostgreSQL 12+ 
- Python 3.10+
- Virtual environment активирован

---

## 🚀 **Быстрая установка (Windows):**

### **Шаг 1: Установить PostgreSQL**

**Скачать:**
- https://www.postgresql.org/download/windows/
- Или через Chocolatey: `choco install postgresql`

**После установки:**
```bash
# Запустить PostgreSQL
pg_ctl start

# Или через службы Windows
services.msc → PostgreSQL → Start
```

---

### **Шаг 2: Создать базу данных**

```bash
# Войти в psql
psql -U postgres

# Создать БД
CREATE DATABASE hintsage;

# Создать пользователя (опционально)
CREATE USER hintsage_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE hintsage TO hintsage_user;

# Выйти
\q
```

---

### **Шаг 3: Настроить переменные окружения**

Создать файл `.env` в папке `backend/`:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/hintsage
JWT_SECRET_KEY=your-super-secret-key-min-32-characters-long
```

**Важно:** Замените `your_password` на реальный пароль!

---

### **Шаг 4: Применить миграции**

```bash
# Перейти в папку backend
cd backend

# Активировать venv
venv\Scripts\activate

# Запустить setup скрипт
setup_db.bat
```

**Или вручную:**
```bash
# Применить миграции
alembic upgrade head
```

---

### **Шаг 5: Добавить тестовые данные (опционально)**

```bash
python seed_data.py
```

**Создаст тестовых пользователей:**
- `free@test.com` / `password123` (FREE tier)
- `pro@test.com` / `password123` (PRO tier)
- `enterprise@test.com` / `password123` (ENTERPRISE tier)

---

## 🧪 **Проверка подключения:**

```bash
python -c "from app.database import engine; engine.connect(); print('✅ Connected!')"
```

Если видите `✅ Connected!` - все работает!

---

## 📊 **Структура БД:**

### **Таблицы:**

1. **users** - пользователи
   - id (UUID)
   - email (unique)
   - password_hash
   - name, avatar_url
   - oauth_provider, oauth_id
   - email_verified, is_active
   - timestamps

2. **subscriptions** - подписки
   - id (UUID)
   - user_id (FK → users)
   - tier (FREE/PRO/ENTERPRISE)
   - status (ACTIVE/CANCELED/EXPIRED/TRIAL)
   - tochka_operation_id
   - current_period_start/end
   - timestamps

3. **payments** - платежи
   - id (UUID)
   - user_id (FK → users)
   - tochka_operation_id (unique)
   - amount, purpose
   - status (CREATED/PAID/FAILED/REFUNDED)
   - payment_link
   - subscription_tier, subscription_period
   - tochka_raw_data (JSONB)
   - timestamps

4. **app_versions** - версии приложения
   - id (UUID)
   - version (unique, e.g. "1.0.0")
   - platform (windows/macos/linux)
   - release_date
   - changelog (JSON array)
   - download_url
   - critical (boolean)
   - active (boolean)

---

## 🔧 **Полезные команды:**

### **Alembic:**

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Add new column"

# Применить миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1

# Посмотреть историю
alembic history

# Текущая версия
alembic current
```

### **PostgreSQL:**

```bash
# Подключиться к БД
psql -U postgres -d hintsage

# Показать все таблицы
\dt

# Описать таблицу
\d users

# Показать всех пользователей
SELECT email, name, tier FROM users 
JOIN subscriptions ON users.id = subscriptions.user_id;

# Выйти
\q
```

---

## 🐛 **Troubleshooting:**

### **Проблема: "connection refused"**
```
Решение:
1. Проверить что PostgreSQL запущен
2. Проверить порт (по умолчанию 5432)
3. Проверить DATABASE_URL в .env
```

### **Проблема: "database does not exist"**
```
Решение:
psql -U postgres -c "CREATE DATABASE hintsage;"
```

### **Проблема: "password authentication failed"**
```
Решение:
1. Проверить пароль в DATABASE_URL
2. Сбросить пароль: ALTER USER postgres WITH PASSWORD 'new_password';
```

### **Проблема: Alembic не видит модели**
```
Решение:
1. Убедиться что все модели импортированы в alembic/env.py
2. Проверить что PYTHONPATH настроен правильно
```

---

## ✅ **Готово!**

После успешной настройки БД можно запускать API:

```bash
start.bat
```

API будет доступен на http://localhost:8000

Swagger UI: http://localhost:8000/docs

