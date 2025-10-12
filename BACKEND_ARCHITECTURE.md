
# 🏗️ Backend Architecture - Hintsage

## 📊 **СТАТУС РЕАЛИЗАЦИИ**

### ✅ **ГОТОВО (MVP):**

1. **Структура проекта** - полная структура папок
2. **Конфигурация** (`app/config.py`) - все настройки для РФ
3. **Database** (`app/database.py`) - PostgreSQL подключение
4. **Models** - все модели БД:
   - `user.py` - пользователи
   - `subscription.py` - подписки (FREE/PRO/ENTERPRISE)
   - `payment.py` - платежи (Банк Точка)
   - `app_version.py` - версии приложения
5. **Services** - бизнес-логика:
   - `jwt_service.py` - JWT токены с подпиской
   - `auth_service.py` - регистрация/вход
   - `user_service.py` - управление пользователями
   - `payment_service.py` - интеграция с Банком Точка
   - `subscription_service.py` - управление подписками
6. **Main App** (`app/main.py`) - FastAPI приложение
7. **Requirements** - все зависимости
8. **Environment** - пример `.env` с реальными данными Банка Точка

---

## 🔧 **ЧТО НУЖНО ДОДЕЛАТЬ:**

### **1. Pydantic Schemas** (30 мин)
```
app/schemas/
├── auth.py        # RegisterRequest, LoginRequest, TokenResponse
├── user.py        # UserResponse, UserUpdate
├── payment.py     # PaymentCreate, PaymentResponse
└── subscription.py # SubscriptionResponse
```

### **2. API Endpoints** (1 час)
```
app/api/v1/
├── auth.py        # POST /register, /login, /refresh
├── users.py       # GET /me, PUT /me
├── payments.py    # POST /create, GET /{id}, POST /webhooks/tochka
└── version.py     # POST /check
```

### **3. Middleware** (15 мин)
```
app/middleware/
└── auth.py        # JWT authentication middleware
```

### **4. Database Migrations** (15 мин)
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial"
alembic upgrade head
```

---

## 🚀 **БЫСТРЫЙ СТАРТ**

### **1. Установка:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### **2. Настройка БД:**
```bash
# Установить PostgreSQL
# Создать базу данных
createdb hintsage

# Применить миграции
alembic upgrade head
```

### **3. Переменные окружения:**
Создать `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/hintsage
JWT_SECRET_KEY=your-super-secret-key-min-32-characters
TOCHKA_BEARER_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
```

### **4. Запуск:**
```bash
uvicorn app.main:app --reload --port 8000
```

API доступен: `http://localhost:8000`

---

## 💳 **Банк Точка - Настройки**

### **Credentials (из env):**
```
API URL: https://enter.tochka.com/uapi
Bearer Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
Customer Code: 305047981
Merchant ID: 200000000021710
Client ID: cdd1617ed04d6e0338aee818b6d74544
```

### **Webhook URL:**
```
https://smartsobes.ru/api/v1/webhooks/tochka
```

---

## 🔐 **JWT Token Структура**

```json
{
  "sub": "user_uuid",
  "email": "user@example.com",
  "name": "User Name",
  "tier": "pro",
  "features": [
    "advanced_stt",
    "unlimited_requests",
    "extended_context",
    "custom_prompts"
  ],
  "subscription_status": "active",
  "subscription_end": "2025-11-12T00:00:00Z",
  "exp": 1234567890
}
```

---

## 📱 **Desktop App Integration**

### **Auth Flow:**
```
1. Desktop App → Открыть браузер с URL:
   https://smartsobes.ru/login?callback=hintsage://auth

2. User → Ввести email/password

3. Backend → Генерировать JWT

4. Frontend → Redirect to: hintsage://auth?token=JWT_TOKEN

5. Desktop App → Перехватить URL, извлечь token

6. Desktop App → Decode JWT, получить tier + features

7. Desktop App → Активировать/деактивировать функции
```

---

## 🎯 **Feature Flags по Tier**

### **FREE:**
- `basic_stt` - только Vosk
- `limited_requests` - 5 запросов/час
- `standard_context` - стандартный контекст

### **PRO ($1499/мес):**
- `advanced_stt` - Whisper GPU
- `unlimited_requests`
- `extended_context`
- `custom_prompts`
- `priority_support`
- `screenshot_ocr`

### **ENTERPRISE ($7490/мес):**
- Все из PRO +
- `team_sharing`
- `custom_integrations`
- `dedicated_support`

---

## 🧪 **Тестирование API**

### **Регистрация:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "secure_password",
    "name": "Test User"
  }'
```

### **Вход:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "secure_password"
  }'
```

### **Создание платежа:**
```bash
curl -X POST http://localhost:8000/api/v1/payments/create \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tier": "pro",
    "period": "monthly"
  }'
```

---

## 📦 **Deployment**

### **Railway (рекомендуется для старта):**
```bash
railway login
railway init
railway up
railway add postgresql redis
```

### **Docker:**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔗 **Следующие шаги:**

1. ✅ **Доделать Schemas + Endpoints** (1-2 часа)
2. ✅ **Тестирование** (30 мин)
3. ✅ **Frontend Landing** (2-3 часа)
4. ✅ **Desktop App Integration** (1-2 часа)
5. ✅ **Deployment** (1 час)

**ИТОГО:** ~7-10 часов до полного MVP

---

## 📝 **Контакты и Support:**

- **Email:** support@smartsobes.ru
- **Domain:** smartsobes.ru
- **Backend API:** api.smartsobes.ru (или smartsobes.ru/api)


