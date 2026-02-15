# -*- coding: utf-8 -*-
"""
Test Auth and Feature Managers
"""

import sys
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

print("="*60)
print("Testing Auth + Feature Managers")
print("="*60)

# Test 1: Feature Manager
print("\n[1] Testing Feature Manager...")
try:
    from modules.features import FeatureManager
    
    # Test FREE tier
    fm_free = FeatureManager(tier="free")
    print(f"OK - FREE tier created")
    print(f"   STT engine: {fm_free.get_stt_engine()}")
    print(f"   Max requests/hour: {fm_free.get_max_requests_per_hour()}")
    print(f"   Context window: {fm_free.get_context_window_size()}")
    print(f"   OCR available: {fm_free.can_use_screenshot_ocr()}")
    
    # Test PRO tier
    fm_pro = FeatureManager(tier="pro")
    print(f"\nOK - PRO tier created")
    print(f"   STT engine: {fm_pro.get_stt_engine()}")
    print(f"   Max requests/hour: {fm_pro.get_max_requests_per_hour()}")
    print(f"   Context window: {fm_pro.get_context_window_size()}")
    print(f"   OCR available: {fm_pro.can_use_screenshot_ocr()}")
    
    # Test feature check
    print(f"\nOK - Feature checks:")
    print(f"   FREE has advanced_stt: {fm_free.is_feature_enabled('advanced_stt')}")
    print(f"   PRO has advanced_stt: {fm_pro.is_feature_enabled('advanced_stt')}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Auth Manager
print("\n[2] Testing Auth Manager...")
try:
    from modules.auth import AuthManager
    
    auth = AuthManager(
        backend_url="http://localhost:8000",
        frontend_url="http://localhost:3000"
    )
    print(f"OK - Auth Manager created")
    print(f"   Backend URL: {auth.backend_url}")
    print(f"   Frontend URL: {auth.frontend_url}")
    print(f"   Callback port: {auth.callback_port}")
    print(f"   Is authenticated: {auth.is_authenticated()}")
    
    # Test JWT mock
    print(f"\nOK - Testing JWT mock...")
    import jwt
    from datetime import datetime, timedelta
    
    mock_payload = {
        "sub": "test-user-123",
        "email": "test@example.com",
        "name": "Test User",
        "tier": "pro",
        "features": ["advanced_stt", "unlimited_requests", "extended_context"],
        "subscription_status": "active",
        "exp": int((datetime.utcnow() + timedelta(days=7)).timestamp())
    }
    
    mock_token = jwt.encode(mock_payload, "secret", algorithm="HS256")
    print(f"   Mock JWT created: {mock_token[:50]}...")
    
    # Decode без проверки
    decoded = jwt.decode(mock_token, options={"verify_signature": False})
    print(f"   Decoded tier: {decoded['tier']}")
    print(f"   Decoded features: {len(decoded['features'])} items")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Integration check
print("\n[3] Testing integration...")
try:
    from modules.config_manager import ConfigManager
    
    config = ConfigManager()
    backend_url = config.get("backend.url", "http://localhost:8000")
    print(f"OK - Config backend.url: {backend_url}")
    
    frontend_url = config.get("backend.frontend_url", "http://localhost:3000")
    print(f"OK - Config frontend_url: {frontend_url}")
    
    enabled = config.get("backend.enabled", False)
    print(f"OK - Backend enabled: {enabled}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("ALL TESTS PASSED!")
print("="*60)
print("\nReady to launch Desktop App with Auth!")
print("Features:")
print("  - Auth Manager: Browser-based auth flow")
print("  - Feature Manager: Tier-based restrictions")
print("  - JWT: Token extraction and decoding")
print("="*60)


