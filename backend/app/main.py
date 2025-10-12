"""
FastAPI Main Application - [АЗ + ДОБРО]
Основное приложение Backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import init_db

settings = get_settings()

# Создаем FastAPI app
app = FastAPI(
    title="Hintsage API",
    description="Backend API для Hintsage - AI Interview Assistant",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация БД при старте
@app.on_event("startup")
async def startup_event():
    """Инициализация при старте"""
    init_db()
    print("✅ Database initialized")
    print(f"✅ Hintsage Backend API запущен на {settings.API_V1_PREFIX}")

# Health check
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": "Hintsage Backend API",
        "version": settings.APP_VERSION,
        "status": "online"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Import and include routers
from app.api.v1 import auth, users, payments, version

app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["users"])
app.include_router(payments.router, prefix=f"{settings.API_V1_PREFIX}/payments", tags=["payments"])
app.include_router(version.router, prefix=f"{settings.API_V1_PREFIX}/version", tags=["version"])

