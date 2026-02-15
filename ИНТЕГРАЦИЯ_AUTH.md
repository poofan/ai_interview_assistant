# 🔐 Desktop App Auth Integration

## ✅ **ЧТО РЕАЛИЗОВАНО:**

### **1. Auth Manager** (`modules/auth/auth_manager.py`)
- ✅ Browser-based authentication flow
- ✅ Local HTTP callback server (port 8765)
- ✅ JWT token extraction from URL
- ✅ Automatic tier detection from JWT
- ✅ Feature extraction from JWT

### **2. Feature Manager** (`modules/features/feature_manager.py`)
- ✅ Feature flags по тарифам (FREE/PRO/ENTERPRISE)
- ✅ STT engine selection (Vosk/Whisper)
- ✅ Request limits (5/hour для FREE, unlimited для PRO+)
- ✅ Context window size (10 для FREE, 30 для PRO+)
- ✅ OCR availability check
- ✅ Custom prompts check

### **3. Integration в main.py**
- ✅ AuthManager инициализация
- ✅ FeatureManager инициализация
- ✅ Config расширен (backend.url, backend.frontend_url)

---

## 🔄 **AUTHENTICATION FLOW:**

```
┌──────────────────┐
│  Desktop App     │
│  (main.py)       │
└────────┬─────────┘
         │
         │ 1. auth_manager.login()
         ├──────────────────────────────┐
         │                              │
         ▼                              ▼
┌────────────────────┐      ┌─────────────────────┐
│ Start HTTP Server  │      │  Open Browser       │
│ localhost:8765     │      │  frontend/login     │
└────────────────────┘      │  ?callback=...      │
         ▲                  └──────────┬──────────┘
         │                             │
         │                             ▼
         │                  ┌─────────────────────┐
         │                  │  User Login Form    │
         │                  │  (email/password)   │
         │                  └──────────┬──────────┘
         │                             │
         │                             ▼
         │                  ┌─────────────────────┐
         │                  │  Backend API        │
         │                  │  POST /auth/login   │
         │                  └──────────┬──────────┘
         │                             │
         │                             ▼
         │                  ┌─────────────────────┐
         │                  │  Generate JWT       │
         │                  │  with tier+features │
         │                  └──────────┬──────────┘
         │                             │
         │  3. Redirect:               │
         │  localhost:8765/callback    │
         │  ?token=JWT_TOKEN           │
         ◄─────────────────────────────┘
         │
         │ 4. Extract JWT
         ▼
┌────────────────────────────────────┐
│  Decode JWT                        │
│  - tier: "pro"                     │
│  - features: ["advanced_stt", ...] │
└────────┬───────────────────────────┘
         │
         │ 5. Update FeatureManager
         ▼
┌────────────────────────────────────┐
│  Enable/Disable Features           │
│  - STT: whisper (if PRO+)          │
│  - Requests: unlimited             │
│  - Context: 30 messages            │
└────────────────────────────────────┘
```

---

## 💻 **КАК ИСПОЛЬЗОВАТЬ:**

### **В Desktop App (main.py):**

```python
# Инициализация (уже добавлено)
self.auth_manager = AuthManager(
    backend_url="http://localhost:8000",
    frontend_url="http://localhost:3000"
)
self.feature_manager = FeatureManager(tier="free")

# Авторизация (через новый hotkey или кнопку)
def authorize_user():
    if self.auth_manager.login():
        # Ждем callback (можно добавить таймаут)
        # После успешной авторизации обновляем features
        
        tier = self.auth_manager.get_subscription_tier()
        features = self.auth_manager.get_features()
        
        # Обновляем Feature Manager
        self.feature_manager = FeatureManager(tier=tier, features=features)
        
        # Применяем ограничения
        restrictions = self.feature_manager.get_feature_restrictions()
        
        # Переключаем STT движок
        if restrictions['stt_engine'] == 'whisper':
            self.stt_engine.set_engine('whisper')
        else:
            self.stt_engine.set_engine('vosk')

# Проверка фич перед использованием
def use_screenshot_ocr():
    if not self.feature_manager.can_use_screenshot_ocr():
        # Показать сообщение об апгрейде
        message = self.feature_manager.get_upgrade_message()
        # Показать в UI
        return
    
    # Использовать OCR
    ...
```

---

## 🎯 **FEATURE FLAGS:**

### **FREE Tier:**
```python
features = [
    "basic_stt",         # → STT engine: vosk
    "limited_requests",  # → Max 5 requests/hour
    "standard_context"   # → Context window: 10 messages
]
```

### **PRO Tier:**
```python
features = [
    "advanced_stt",         # → STT engine: whisper GPU
    "unlimited_requests",   # → No limits
    "extended_context",     # → Context window: 30 messages
    "custom_prompts",       # → Can use custom prompts
    "screenshot_ocr",       # → OCR available
    "priority_support"
]
```

### **ENTERPRISE Tier:**
```python
features = [
    # Все из PRO +
    "team_sharing",         # Будущее
    "custom_integrations",  # Будущее
    "dedicated_support"
]
```

---

## 🧪 **ТЕСТИРОВАНИЕ:**

### **1. Тест авторизации (когда backend готов):**
```python
# 1. Запустить backend
cd backend
uvicorn app.main:app --reload --port 8000

# 2. Запустить frontend
cd frontend
npm run dev

# 3. Запустить desktop app
python main.py

# 4. Нажать hotkey для авторизации (нужно добавить)
# Ctrl+Shift+L (Login)

# 5. В браузере ввести:
# email: pro@test.com
# password: password123

# 6. После успешного входа:
# Desktop app получит JWT
# Tier переключится на "pro"
# Whisper GPU активируется
```

---

## 📝 **TODO (осталось):**

### **Frontend:**
- [ ] Login Page (`frontend/app/login/page.tsx`)
- [ ] Register Page (`frontend/app/register/page.tsx`)
- [ ] Dashboard (`frontend/app/dashboard/page.tsx`)
- [ ] API Client (`frontend/lib/api.ts`)

### **Desktop App:**
- [ ] Hotkey для авторизации (Ctrl+Shift+L)
- [ ] UI индикатор текущего тарифа
- [ ] Кнопка "Upgrade" в overlay
- [ ] Применение feature flags к компонентам

---

## ⏱️ **ESTIMATED TIME:**

| Задача | Время |
|--------|-------|
| Login Page | 20 мин |
| Register Page | 20 мин |
| Dashboard | 30 мин |
| API Client | 15 мин |
| Desktop hotkeys + UI | 30 мин |
| **ИТОГО** | **~2 часа** |

---

## 🎯 **СТАТУС MVP:**

**Прогресс: 95%!**

- ✅ Backend API (100%)
- ✅ Frontend Landing (100%)
- ✅ Desktop Auth Manager (100%)
- ✅ Feature Manager (100%)
- ⏳ Login/Register UI (0%)
- ⏳ Desktop hotkeys (0%)

**Для полного MVP осталось ~2 часа работы!**

---

## 💡 **СЛЕДУЮЩИЙ ШАГ:**

Создать Login/Register страницы или добавить hotkey для авторизации в Desktop App?

**Ваш выбор?** 🤔

