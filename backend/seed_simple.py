# -*- coding: utf-8 -*-
"""Simple Seed Data"""

from app.database import SessionLocal
from app.models.user import User
from app.models.subscription import Subscription, SubscriptionTier, SubscriptionStatus
from app.models.app_version import AppVersion
from datetime import datetime, timedelta
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed():
    db = SessionLocal()
    
    try:
        print("Seeding database...")
        
        # 1. FREE user
        print("\n1. Creating FREE user...")
        user_free = User(
            id=uuid.uuid4(),
            email="free@test.com",
            password_hash=pwd_context.hash("password123"),
            name="Free User",
            email_verified=True,
            is_active=True
        )
        db.add(user_free)
        db.flush()
        
        sub_free = Subscription(
            user_id=user_free.id,
            tier=SubscriptionTier.FREE,
            status=SubscriptionStatus.ACTIVE
        )
        db.add(sub_free)
        print(f"   Created: {user_free.email}")
        
        # 2. PRO user
        print("\n2. Creating PRO user...")
        user_pro = User(
            id=uuid.uuid4(),
            email="pro@test.com",
            password_hash=pwd_context.hash("password123"),
            name="Pro User",
            email_verified=True,
            is_active=True
        )
        db.add(user_pro)
        db.flush()
        
        sub_pro = Subscription(
            user_id=user_pro.id,
            tier=SubscriptionTier.PRO,
            status=SubscriptionStatus.ACTIVE,
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=30)
        )
        db.add(sub_pro)
        print(f"   Created: {user_pro.email}")
        
        # 3. ENTERPRISE user
        print("\n3. Creating ENTERPRISE user...")
        user_ent = User(
            id=uuid.uuid4(),
            email="enterprise@test.com",
            password_hash=pwd_context.hash("password123"),
            name="Enterprise User",
            email_verified=True,
            is_active=True
        )
        db.add(user_ent)
        db.flush()
        
        sub_ent = Subscription(
            user_id=user_ent.id,
            tier=SubscriptionTier.ENTERPRISE,
            status=SubscriptionStatus.ACTIVE,
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=365)
        )
        db.add(sub_ent)
        print(f"   Created: {user_ent.email}")
        
        # 4. App version
        print("\n4. Creating app version...")
        app_ver = AppVersion(
            version="1.0.0",
            platform="windows",
            release_date=datetime.utcnow(),
            changelog='["First release", "GPU acceleration", "Auth system"]',
            download_url="https://smartsobes.ru/download/Hintsage-1.0.0.exe",
            file_size="45.2 MB",
            critical=False,
            min_version="1.0.0",
            active=True
        )
        db.add(app_ver)
        print(f"   Created version: 1.0.0")
        
        db.commit()
        
        print("\n" + "="*50)
        print("DATABASE SEEDED SUCCESSFULLY!")
        print("="*50)
        print("\nTest users:")
        print("  free@test.com / password123 (FREE)")
        print("  pro@test.com / password123 (PRO)")
        print("  enterprise@test.com / password123 (ENTERPRISE)")
        print("\nReady to test!")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed()

