"""
Seed Data - Тестовые данные для разработки
"""

from app.database import SessionLocal
from app.models.user import User
from app.models.subscription import Subscription, SubscriptionTier, SubscriptionStatus
from app.models.app_version import AppVersion
from datetime import datetime, timedelta
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    """Заполнить БД тестовыми данными"""
    db = SessionLocal()
    
    try:
        print("🌱 Seeding database with test data...")
        
        # 1. Создать тестового пользователя FREE
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
        
        subscription_free = Subscription(
            user_id=user_free.id,
            tier=SubscriptionTier.FREE,
            status=SubscriptionStatus.ACTIVE
        )
        db.add(subscription_free)
        print(f"   ✅ Created: {user_free.email} (password: password123)")
        
        # 2. Создать тестового пользователя PRO
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
        
        subscription_pro = Subscription(
            user_id=user_pro.id,
            tier=SubscriptionTier.PRO,
            status=SubscriptionStatus.ACTIVE,
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=30)
        )
        db.add(subscription_pro)
        print(f"   ✅ Created: {user_pro.email} (password: password123)")
        
        # 3. Создать тестового пользователя ENTERPRISE
        print("\n3. Creating ENTERPRISE user...")
        user_enterprise = User(
            id=uuid.uuid4(),
            email="enterprise@test.com",
            password_hash=pwd_context.hash("password123"),
            name="Enterprise User",
            email_verified=True,
            is_active=True
        )
        db.add(user_enterprise)
        db.flush()
        
        subscription_enterprise = Subscription(
            user_id=user_enterprise.id,
            tier=SubscriptionTier.ENTERPRISE,
            status=SubscriptionStatus.ACTIVE,
            current_period_start=datetime.utcnow(),
            current_period_end=datetime.utcnow() + timedelta(days=365)
        )
        db.add(subscription_enterprise)
        print(f"   ✅ Created: {user_enterprise.email} (password: password123)")
        
        # 4. Создать текущую версию приложения
        print("\n4. Creating app version...")
        app_version = AppVersion(
            version="1.0.0",
            platform="windows",
            release_date=datetime.utcnow(),
            changelog='["✨ Первый релиз Hintsage", "🎯 GPU ускорение для STT", "🔐 Система авторизации"]',
            download_url="https://smartsobes.ru/download/Hintsage-1.0.0.exe",
            file_size="45.2 MB",
            critical=False,
            min_version="1.0.0",
            active=True
        )
        db.add(app_version)
        print(f"   ✅ Created version: {app_version.version}")
        
        # Commit всех изменений
        db.commit()
        
        print("\n" + "="*50)
        print("✅ Database seeded successfully!")
        print("="*50)
        print("\nTest users:")
        print("  FREE:       free@test.com / password123")
        print("  PRO:        pro@test.com / password123")
        print("  ENTERPRISE: enterprise@test.com / password123")
        print("\nYou can now test the API with these credentials!")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

