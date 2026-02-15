"""
Database Connection - [АЗ + ДОБРО]
Подключение к PostgreSQL и управление сессиями
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.config import get_settings

settings = get_settings()

# Создаем engine для PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_size=10,
    max_overflow=20
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency для получения DB сессии
    
    Yields:
        Session: SQLAlchemy сессия
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Инициализация БД (создание таблиц)
    """
    # Импортируем все модели
    from app.models import user, subscription, app_version
    
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)

