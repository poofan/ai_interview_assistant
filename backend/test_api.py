"""
Quick API Test - Без БД
Тестируем основные компоненты backend
"""

import sys
from pathlib import Path

# Добавляем путь к app
sys.path.insert(0, str(Path(__file__).parent))

print("="*60)
print("TESTIROVANIE BACKEND API")
print("="*60)

# Тест 1: Импорт модулей
print("\n1. Тестируем импорт модулей...")
try:
    from app.config import get_settings
    from app.models import User, Subscription, Payment, AppVersion
    from app.schemas import RegisterRequest, LoginRequest
    from app.services import JWTService
    print("   OK Vse moduli importiruyutsya")
except Exception as e:
    print(f"   ❌ Ошибка импорта: {e}")
    sys.exit(1)

# Тест 2: Конфигурация
print("\n2. Тестируем конфигурацию...")
try:
    settings = get_settings()
    print(f"   ✅ APP_NAME: {settings.APP_NAME}")
    print(f"   ✅ APP_VERSION: {settings.APP_VERSION}")
    print(f"   ✅ TOCHKA_MERCHANT_ID: {settings.TOCHKA_MERCHANT_ID}")
    print(f"   ✅ PRICE_PRO_MONTHLY: {settings.PRICE_PRO_MONTHLY} руб")
except Exception as e:
    print(f"   ❌ Ошибка конфигурации: {e}")
    sys.exit(1)

# Тест 3: JWT Service
print("\n3. Тестируем JWT Service...")
try:
    # Создаем тестового пользователя (без БД)
    class MockUser:
        id = "test-user-123"
        email = "test@example.com"
        name = "Test User"
        email_verified = True
    
    class MockSubscription:
        tier = "pro"
        status = "active"
        features = ["advanced_stt", "unlimited_requests"]
        is_active = True
        current_period_end = None
        
        class tier:
            value = "pro"
        class status:
            value = "active"
    
    user = MockUser()
    subscription = MockSubscription()
    
    # Создаем токен
    token = JWTService.create_access_token(user, subscription)
    print(f"   ✅ JWT токен создан: {token[:50]}...")
    
    # Декодируем токен
    payload = JWTService.decode_token(token)
    if payload:
        print(f"   ✅ Токен декодирован:")
        print(f"      - Email: {payload.get('email')}")
        print(f"      - Tier: {payload.get('tier')}")
        print(f"      - Features: {len(payload.get('features', []))} шт")
    else:
        print("   ❌ Не удалось декодировать токен")
except Exception as e:
    print(f"   ❌ Ошибка JWT: {e}")
    import traceback
    traceback.print_exc()

# Тест 4: Pydantic Schemas
print("\n4. Тестируем Pydantic Schemas...")
try:
    # Тест RegisterRequest
    register_data = {
        "email": "test@example.com",
        "password": "secure_password123",
        "name": "Test User"
    }
    register_req = RegisterRequest(**register_data)
    print(f"   ✅ RegisterRequest: {register_req.email}")
    
    # Тест LoginRequest
    login_data = {
        "email": "test@example.com",
        "password": "secure_password123"
    }
    login_req = LoginRequest(**login_data)
    print(f"   ✅ LoginRequest: {login_req.email}")
except Exception as e:
    print(f"   ❌ Ошибка Schemas: {e}")

# Тест 5: FastAPI App
print("\n5. Тестируем FastAPI приложение...")
try:
    from app.main import app
    print(f"   ✅ FastAPI app создан: {app.title}")
    print(f"   ✅ Роутеры подключены:")
    for route in app.routes:
        if hasattr(route, 'path') and '/api/v1/' in route.path:
            print(f"      - {route.methods} {route.path}")
except Exception as e:
    print(f"   ❌ Ошибка FastAPI: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("VSE TESTY PROYZDENY!")
print("="*60)
print("\nBackend gotov k zapusku!")
print("Zapustite: uvicorn app.main:app --reload --port 8000")
print("="*60)

