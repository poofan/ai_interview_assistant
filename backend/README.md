# 🚀 Hintsage Backend API

FastAPI backend для системы авторизации и управления подписками Hintsage.

---

## 📋 Технологии

- **FastAPI** - современный async web framework
- **PostgreSQL** - основная база данных
- **Redis** - кэш и сессии
- **SQLAlchemy** - ORM
- **Alembic** - миграции БД
- **JWT** - авторизация
- **Банк Точка** - платежная система (РФ)

---

## 🏗️ Структура

```
backend/
├── app/
│   ├── api/v1/           # API endpoints
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   ├── middleware/       # Middleware
│   ├── utils/            # Utilities
│   ├── config.py         # Configuration
│   ├── database.py       # DB connection
│   └── main.py           # FastAPI app
├── alembic/              # DB migrations
├── tests/                # Tests
├── requirements.txt
└── README.md
```

---

## 🚀 Установка

### 1. Создать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Установить зависимости:
```bash
pip install -r requirements.txt
```

### 3. Настроить переменные окружения:
```bash
cp env.example .env
# Отредактировать .env с вашими данными
```

### 4. Инициализировать БД:
```bash
alembic upgrade head
```

### 5. Запустить сервер:
```bash
uvicorn app.main:app --reload --port 8000
```

API будет доступен по адресу: `http://localhost:8000`

---

## 📊 API Endpoints

### **Authentication:**
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход
- `POST /api/v1/auth/refresh` - Обновление токена
- `POST /api/v1/auth/forgot-password` - Восстановление пароля
- `POST /api/v1/auth/reset-password` - Сброс пароля

### **Users:**
- `GET /api/v1/users/me` - Текущий пользователь
- `PUT /api/v1/users/me` - Обновить профиль
- `GET /api/v1/users/me/subscription` - Информация о подписке

### **Payments:**
- `POST /api/v1/payments/create` - Создать платеж
- `GET /api/v1/payments/{operation_id}` - Статус платежа
- `POST /api/v1/webhooks/tochka` - Webhook от Банка Точка

### **Versions:**
- `POST /api/v1/version/check` - Проверка обновлений

---

## 💳 Интеграция с Банком Точка

### Тестовые данные:
```json
{
  "customerCode": "300000092",
  "merchantId": "200000000001056"
}
```

### Webhook URL:
```
https://smartsobes.ru/api/v1/webhooks/tochka
```

---

## 🔐 JWT Структура

```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "name": "User Name",
  "tier": "pro",
  "features": ["advanced_stt", "unlimited_requests"],
  "subscription_status": "active",
  "exp": 1234567890
}
```

---

## 🧪 Тестирование

```bash
pytest tests/
```

---

## 📦 Деплой

### На Railway:
```bash
railway login
railway init
railway up
```

### На своем сервере:
```bash
# Установить PostgreSQL и Redis
sudo apt install postgresql redis-server

# Настроить systemd service
sudo cp hintsage-backend.service /etc/systemd/system/
sudo systemctl enable hintsage-backend
sudo systemctl start hintsage-backend
```

---

## 📝 TODO

- [ ] Добавить OAuth (Google, GitHub)
- [ ] Реализовать email уведомления
- [ ] Добавить rate limiting
- [ ] Настроить мониторинг (Sentry)
- [ ] Документация API (Swagger)
- [ ] CI/CD pipeline

---

## 🔗 Полезные ссылки

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Банк Точка API](https://enter.tochka.com/)

