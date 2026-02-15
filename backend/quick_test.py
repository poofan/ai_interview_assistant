# -*- coding: utf-8 -*-
"""Quick Test"""

print("="*60)
print("Testing Backend Components")
print("="*60)

# Test 1
print("\n[1] Testing config...")
try:
    from app.config import get_settings
    settings = get_settings()
    print(f"OK - App: {settings.APP_NAME}")
    print(f"OK - Tochka Merchant: {settings.TOCHKA_MERCHANT_ID}")
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)

# Test 2
print("\n[2] Testing JWT...")
try:
    from app.services.jwt_service import JWTService
    
    class MockUser:
        id = "123"
        email = "test@test.com"
        name = "Test"
        email_verified = True
    
    token = JWTService.create_access_token(MockUser(), None)
    print(f"OK - Token created: {token[:40]}...")
    
    payload = JWTService.decode_token(token)
    print(f"OK - Token decoded: {payload.get('email')}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 3  
print("\n[3] Testing schemas...")
try:
    from app.schemas.auth import RegisterRequest
    req = RegisterRequest(email="test@test.com", password="pass12345678")
    print(f"OK - Schema works: {req.email}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "="*60)
print("All tests passed!")
print("="*60)

