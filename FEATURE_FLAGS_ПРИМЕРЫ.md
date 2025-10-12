# 🎛️ Feature Flags - Адаптация UI под подписку

> **Как приложение адаптируется под тариф пользователя**

---

## 📊 **СРАВНЕНИЕ ТАРИФОВ**

| Фича | FREE | PRO | ENTERPRISE |
|------|------|-----|------------|
| **Запросов/день** | 10 | 500 | Unlimited |
| **OCR (скриншоты)** | ❌ | ✅ | ✅ |
| **Аудио режим** | Только микрофон | Оба (mic+собеседник) | Оба |
| **Контекст** | 3,000 токенов | 10,000 токенов | 50,000 токенов |
| **Ответ (max_tokens)** | 500 | 2,000 | 8,000 |
| **Параллельные запросы** | 1 | 3 | 10 |
| **Расширенные промпты** | ❌ | ✅ | ✅ |
| **Экспорт истории** | ❌ | ✅ | ✅ |
| **Кастомный UI** | ❌ | ✅ | ✅ |
| **API доступ** | ❌ | ❌ | ✅ |
| **Поддержка** | Email | Chat | Dedicated |

---

## 💻 **КАК ЭТО РАБОТАЕТ В КОДЕ**

### **1. Загрузка фич из JWT**

```python
# main.py

from modules.auth import AuthManager, FeatureManager

def main():
    # Авторизация
    auth_manager = AuthManager()
    if not auth_manager.is_authenticated():
        # Показать форму входа
        login_dialog = LoginDialog(auth_manager)
        if not login_dialog.exec():
            return
    
    # Загрузить фичи из JWT
    features = auth_manager.get_features()
    feature_manager = FeatureManager(features)
    
    # Показать пользователю его тариф
    tier = features.get("tier", "FREE")
    logger.info(f"🎯 Тариф: {tier}")
    
    # Запуск приложения с ограничениями
    app = HintsageApp(qt_app, feature_manager)
    app.start()
```

---

### **2. Проверка доступа к фичам**

```python
# modules/auth/feature_manager.py

class FeatureManager:
    """Управляет доступом к функциям"""
    
    def __init__(self, features: dict):
        self.features = features
        self.tier = features.get("tier", "FREE")
    
    # OCR
    def can_use_ocr(self) -> bool:
        return self.features.get("ocr_enabled", False)
    
    # Аудио режим
    def get_audio_mode(self) -> str:
        """Возвращает: 'microphone' или 'both'"""
        return self.features.get("audio_mode", "microphone")
    
    # Лимиты
    def get_max_requests_per_day(self) -> int:
        return self.features.get("max_requests_per_day", 10)
    
    def get_context_window(self) -> int:
        return self.features.get("context_window", 3000)
    
    def get_max_tokens(self) -> int:
        return self.features.get("max_tokens", 500)
    
    def get_parallel_workers(self) -> int:
        return self.features.get("parallel_workers", 1)
    
    # Расширенные фичи
    def can_use_advanced_prompts(self) -> bool:
        return self.features.get("advanced_prompts", False)
    
    def can_export_history(self) -> bool:
        return self.features.get("export_history", False)
    
    # UI
    def get_tier_badge(self) -> str:
        """Возвращает значок для UI"""
        badges = {
            "FREE": "🆓 FREE",
            "PRO": "⭐ PRO",
            "ENTERPRISE": "💎 ENTERPRISE"
        }
        return badges.get(self.tier, "🆓")
```

---

### **3. Адаптация конфигурации**

```python
# main.py - в HintsageApp.__init__()

def __init__(self, qt_app, feature_manager):
    super().__init__()
    self.feature_manager = feature_manager
    
    # Загружаем базовую конфигурацию
    self.config = ConfigManager("config.yaml")
    
    # АДАПТИРУЕМ под подписку
    self._adapt_config_to_subscription()
    
    # Остальная инициализация...

def _adapt_config_to_subscription(self):
    """Переопределяет конфиг на основе подписки"""
    
    # 1. Контекстное окно
    context_window = self.feature_manager.get_context_window()
    self.config.set("context.context_window", context_window)
    logger.info(f"📝 Context window: {context_window}")
    
    # 2. Max tokens
    max_tokens = self.feature_manager.get_max_tokens()
    self.config.set("openai.max_tokens", max_tokens)
    logger.info(f"🎯 Max tokens: {max_tokens}")
    
    # 3. Параллельные воркеры
    workers = self.feature_manager.get_parallel_workers()
    self.config.set("parallel.max_workers", workers)
    logger.info(f"⚡ Parallel workers: {workers}")
    
    # 4. Аудио режим
    audio_mode = self.feature_manager.get_audio_mode()
    if audio_mode == "microphone":
        # Принудительно только микрофон
        self.config.set("audio.source", "microphone")
        logger.warning("🎤 Audio: microphone only (upgrade to PRO for 'both')")
    
    # 5. OCR
    if not self.feature_manager.can_use_ocr():
        # Отключаем OCR
        self.config.set("ocr.enabled", False)
        logger.warning("📷 OCR disabled (upgrade to PRO)")
```

---

### **4. Блокировка функций в UI**

```python
# modules/ui_overlay/overlay_window.py

class OverlayWindow(QMainWindow):
    
    def __init__(self, feature_manager):
        super().__init__()
        self.feature_manager = feature_manager
        self._setup_ui()
    
    def _setup_ui(self):
        # ... базовый UI ...
        
        # Показываем тариф
        self._add_tier_badge()
        
        # Показываем лимиты
        self._add_usage_indicator()
    
    def _add_tier_badge(self):
        """Значок тарифа в углу"""
        tier_label = QLabel(self.feature_manager.get_tier_badge())
        tier_label.setStyleSheet("""
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
        """)
        # Добавляем в правый верхний угол
        self.statusBar().addPermanentWidget(tier_label)
    
    def _add_usage_indicator(self):
        """Индикатор использования"""
        max_requests = self.feature_manager.get_max_requests_per_day()
        
        usage_label = QLabel(f"📊 Запросов сегодня: 0/{max_requests}")
        self.statusBar().addWidget(usage_label)
        self.usage_label = usage_label
    
    def update_usage(self, current: int):
        """Обновляет счетчик использования"""
        max_requests = self.feature_manager.get_max_requests_per_day()
        
        self.usage_label.setText(f"📊 Запросов: {current}/{max_requests}")
        
        # Предупреждение при приближении к лимиту
        if max_requests > 0:  # не unlimited
            percentage = (current / max_requests) * 100
            
            if percentage >= 90:
                self.usage_label.setStyleSheet("color: red; font-weight: bold;")
                self._show_upgrade_prompt()
            elif percentage >= 70:
                self.usage_label.setStyleSheet("color: orange;")
    
    def _show_upgrade_prompt(self):
        """Предложение апгрейда"""
        if self.feature_manager.tier != "ENTERPRISE":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Лимит почти исчерпан")
            msg.setText("Вы использовали почти весь дневной лимит!")
            msg.setInformativeText("Апгрейдните подписку для увеличения лимитов")
            
            upgrade_btn = msg.addButton("Upgrade", QMessageBox.ButtonRole.AcceptRole)
            cancel_btn = msg.addButton("Later", QMessageBox.ButtonRole.RejectRole)
            
            msg.exec()
            
            if msg.clickedButton() == upgrade_btn:
                import webbrowser
                webbrowser.open("https://hintsage.com/pricing")
```

---

### **5. Блокировка при превышении лимита**

```python
# main.py - в _manual_trigger()

def _manual_trigger(self):
    """Обработка нажатия триггера"""
    
    # 1. Проверка дневного лимита
    if not self._check_daily_limit():
        return  # Лимит исчерпан
    
    # 2. Проверка параллельных воркеров
    max_workers = self.feature_manager.get_parallel_workers()
    active = self.request_queue.get_active_count()
    
    if active >= max_workers:
        logger.warning(f"⚠️ Max workers reached: {active}/{max_workers}")
        self.overlay_window.show_notification(
            f"⚠️ Достигнут лимит параллельных запросов ({max_workers})\n"
            f"Upgrade to PRO для увеличения"
        )
        return
    
    # 3. Обработка запроса
    # ...

def _check_daily_limit(self) -> bool:
    """Проверяет дневной лимит запросов"""
    max_requests = self.feature_manager.get_max_requests_per_day()
    
    if max_requests == -1:  # unlimited
        return True
    
    # Загружаем счетчик из файла
    today = datetime.now().strftime("%Y-%m-%d")
    usage_file = Path.home() / ".hintsage" / "usage.json"
    
    if usage_file.exists():
        usage = json.loads(usage_file.read_text())
        current = usage.get(today, 0)
    else:
        current = 0
    
    if current >= max_requests:
        # ЛИМИТ ИСЧЕРПАН
        logger.error(f"❌ Daily limit reached: {current}/{max_requests}")
        
        self.overlay_window.show_notification(
            f"❌ Дневной лимит исчерпан ({current}/{max_requests})\n\n"
            f"Upgrade to PRO для увеличения лимита до 500/день"
        )
        
        # Открываем страницу апгрейда
        import webbrowser
        webbrowser.open("https://hintsage.com/pricing")
        
        return False
    
    # Увеличиваем счетчик
    usage[today] = current + 1
    usage_file.parent.mkdir(exist_ok=True)
    usage_file.write_text(json.dumps(usage))
    
    # Обновляем UI
    self.overlay_window.update_usage(current + 1)
    
    return True
```

---

## 🎨 **ВИЗУАЛЬНЫЕ ОТЛИЧИЯ**

### **FREE Tier UI:**
```
┌────────────────────────────────────────┐
│  🆓 FREE                    📊 3/10    │ ← Тариф + лимит
├────────────────────────────────────────┤
│                                        │
│  ⚠️ OCR отключен                       │ ← Предупреждение
│     Upgrade to PRO для скриншотов      │
│                                        │
│  🎤 Только микрофон                    │
│     Upgrade для записи собеседника     │
│                                        │
│  [Ответ LLM]                          │
│                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                        │
│  💡 Upgrade to PRO:                   │
│     ✅ 500 запросов/день               │
│     ✅ OCR скриншотов                  │
│     ✅ Запись обоих (mic+собеседник)  │
│     ✅ 10K контекст                    │
│                                        │
│     [Upgrade Now]                     │
└────────────────────────────────────────┘
```

### **PRO Tier UI:**
```
┌────────────────────────────────────────┐
│  ⭐ PRO                  📊 127/500    │
├────────────────────────────────────────┤
│  ✅ Все функции активны                │
│                                        │
│  [Ответ LLM с полным контекстом]      │
│                                        │
│  📷 OCR: enabled                       │
│  🎤 Audio: both (mic + interviewer)   │
│  📝 Context: 10,000 tokens            │
│  ⚡ Parallel: 3 workers               │
└────────────────────────────────────────┘
```

### **ENTERPRISE Tier UI:**
```
┌────────────────────────────────────────┐
│  💎 ENTERPRISE          📊 Unlimited   │
├────────────────────────────────────────┤
│  🚀 Все функции + API доступ           │
│                                        │
│  [Ответ LLM с расширенным контекстом] │
│                                        │
│  📊 Team Dashboard: 5 members active   │
│  🔧 API Key: sk_live_xxxxx            │
└────────────────────────────────────────┘
```

---

## 🔄 **ПРОВЕРКА ТОКЕНА (каждый час)**

```python
# modules/auth/token_refresher.py

class TokenRefresher(QThread):
    """Фоновое обновление токена"""
    
    token_refreshed = pyqtSignal(dict)  # новые features
    
    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.running = True
    
    def run(self):
        while self.running:
            # Ждем 1 час
            time.sleep(3600)
            
            # Проверяем и обновляем токен
            if self.auth_manager.refresh_if_needed():
                # Загружаем новые features
                features = self.auth_manager.get_features()
                self.token_refreshed.emit(features)
                logger.info("✅ Токен обновлен, features загружены")
```

---

## ✅ **РЕЗЮМЕ**

**JWT токен содержит:**
1. ✅ `tier` - уровень подписки (FREE/PRO/ENTERPRISE)
2. ✅ `features` - детальный список доступных функций
3. ✅ `subscription_id` - ID подписки в Stripe
4. ✅ `expires_at` - дата окончания подписки

**Приложение адаптируется:**
1. ✅ Переопределяет конфиг (context_window, max_tokens, workers)
2. ✅ Блокирует недоступные функции (OCR, audio mode)
3. ✅ Показывает лимиты в UI
4. ✅ Предлагает апгрейд при приближении к лимиту
5. ✅ Автообновляет токен каждый час

---

## 🚀 **ГОТОВЫ К СБОРКЕ?**

Всё это будет реализовано **после сборки .exe**. Сейчас запускаем:

```bash
build.bat
```

**Запускаю?** ⏰ ~10 минут ожидания


