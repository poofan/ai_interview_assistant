# 🧪 E2E Testing Guide - Hintsage MVP

## 🎯 **ЦЕЛЬ ТЕСТИРОВАНИЯ:**

Проверить полный цикл работы:
1. Backend API запускается
2. Frontend Landing отображается
3. Desktop App авторизуется через браузер
4. Feature Flags применяются на основе подписки
5. Все компоненты работают вместе

---

## 🚀 **ПОРЯДОК ЗАПУСКА:**

### **Шаг 1: Запустить Backend API**

```bash
# Терминал 1
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

# Проверка: http://localhost:8000/health
# Должен вернуть: {"status":"healthy"}
```

**Ожидаемый вывод:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
✅ Database initialized
✅ Hintsage Backend API запущен на /api/v1
```

**Время запуска:** ~5 секунд

---

### **Шаг 2: Запустить Frontend**

```bash
# Терминал 2
cd frontend
npm run dev

# Проверка: http://localhost:3000
# Должна открыться Landing Page
```

**Ожидаемый вывод:**
```
▲ Next.js 15.5.4
- Local:        http://localhost:3000
- ready in 2.5s
```

**Время запуска:** ~10-15 секунд

---

### **Шаг 3: Запустить Desktop App**

```bash
# Терминал 3
venv\Scripts\activate
python main.py

# Или через silent launch:
start_silent.vbs
```

**Ожидаемый вывод:**
```
✅ Версия: 1.0.0
✅ AuthManager инициализирован
✅ FeatureManager инициализирован (tier: free)
✅ API ключ валиден
✅ Все компоненты инициализированы
✅ Hintsage запущен!
```

**Время запуска:** ~15-20 секунд

---

## 🧪 **ТЕСТЫ:**

### **Тест 1: Backend Health Check** ✅

```bash
curl http://localhost:8000/health
```

**Ожидаемый ответ:**
```json
{"status":"healthy"}
```

---

### **Тест 2: Backend API Docs** ✅

Открыть в браузере: http://localhost:8000/docs

**Должно быть видно:**
- `/api/v1/auth/register` - POST
- `/api/v1/auth/login` - POST
- `/api/v1/users/me` - GET
- `/api/v1/payments/create` - POST
- `/api/v1/version/check` - POST

---

### **Тест 3: Frontend Landing** ✅

Открыть в браузере: http://localhost:3000

**Должно быть видно:**
- Hero section с градиентным заголовком
- Features (3 карточки: GPU, Security, AI)
- Pricing (FREE 0₽, PRO 1499₽, ENTERPRISE 7490₽)
- Navigation с кнопками "Вход" и "Начать"

---

### **Тест 4: Desktop App Features** ✅

После запуска Desktop App:

1. **Проверить логи:**
   ```
   ✅ FeatureManager инициализирован (tier: free, features: 3)
   ```

2. **Нажать Ctrl+Shift+Q** - ручной триггер
   - Должен работать STT (Vosk для FREE tier)
   - Должен генерировать ответ через OpenAI
   - Ответ должен отображаться в overlay

3. **Проверить ограничения FREE tier:**
   - STT engine: Vosk (не Whisper)
   - Context window: 10 сообщений
   - Requests: 5/hour (не проверяется пока)

---

### **Тест 5: Auth Flow** (требует Login UI)

**ПОКА НЕ РАБОТАЕТ** - нужны Login/Register страницы

Когда Login UI будет готов:

1. Desktop App → Нажать Ctrl+Shift+L (hotkey для авторизации)
2. Откроется браузер → http://localhost:3000/login?callback=...
3. Ввести credentials (например, pro@test.com / password123)
4. Backend → Сгенерирует JWT с tier="pro"
5. Frontend → Redirect на localhost:8765/callback?token=JWT
6. Desktop App → Получит token, обновит tier на "pro"
7. Feature Manager → Переключит STT на Whisper, уберет лимиты

---

## 📊 **ТЕКУЩЕЕ СОСТОЯНИЕ:**

### **✅ Работает:**
- Backend API (localhost:8000)
- Frontend Landing (localhost:3000) 
- Desktop App с Feature Manager
- JWT token handling
- Feature flags (FREE tier активен)

### **⏳ Не работает:**
- Login/Register UI (не созданы)
- Dashboard (не создан)
- Auth flow через браузер (нужен Login UI)
- Upgrade через payment (нужен Dashboard)

---

## 🎯 **СЛЕДУЮЩИЕ ШАГИ:**

### **Для полного E2E теста нужно:**

1. **Создать Login Page** (~20 мин)
   ```typescript
   // frontend/app/login/page.tsx
   - Email/password форма
   - Отправка на POST /api/v1/auth/login
   - Получение JWT
   - Redirect на callback URL
   ```

2. **Создать Register Page** (~20 мин)
   ```typescript
   // frontend/app/register/page.tsx
   - Email/password/name форма
   - Отправка на POST /api/v1/auth/register
   - Автоматический вход после регистрации
   ```

3. **Добавить hotkey в Desktop** (~10 мин)
   ```python
   # main.py
   Ctrl+Shift+L → self.auth_manager.login()
   ```

---

## ⏱️ **ИТОГО ДО ПОЛНОГО E2E:** ~50 минут

---

## 💡 **ВАШ ВЫБОР:**

1. ✅ **Доделать Login/Register** (~40 мин) - для полного E2E
2. 📦 **Собрать .exe сейчас** (~20 мин) - готовый продукт
3. 📝 **Создать финальный отчёт** - подвести итоги

**Что выбираете?** 🤔

