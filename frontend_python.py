#!/usr/bin/env python3
"""
Hintsage - Python Web Frontend
Современный веб-интерфейс на FastAPI + Jinja2
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Optional

# Добавляем путь к модулям
sys.path.append(str(Path(__file__).parent))

try:
    from fastapi import FastAPI, Request, Form, HTTPException, Depends
    from fastapi.responses import HTMLResponse, RedirectResponse
    from fastapi.templating import Jinja2Templates
    from fastapi.staticfiles import StaticFiles
    import uvicorn
except ImportError:
    print("Установите FastAPI: pip install fastapi uvicorn jinja2")
    sys.exit(1)

# Создаем FastAPI приложение
app = FastAPI(
    title="Hintsage - AI Interview Assistant",
    description="Современный веб-интерфейс для Hintsage",
    version="1.0.0"
)

# Настройка шаблонов
templates = Jinja2Templates(directory="templates")

# Backend API URL
BACKEND_URL = "http://localhost:8000"

# HTML шаблоны
LANDING_HTML = """
<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hintsage - AI Interview Assistant</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        gray: {
                            950: '#030712',
                        }
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gray-950 text-white">
    <!-- Navigation -->
    <nav class="fixed top-0 w-full z-50 border-b border-gray-800 bg-gray-950/95 backdrop-blur-xl">
        <div class="max-w-7xl mx-auto px-6">
            <div class="flex items-center justify-between h-16">
                <a href="/" class="text-xl font-semibold text-white">Hintsage</a>
                <div class="hidden md:flex items-center space-x-8">
                    <a href="#features" class="text-gray-400 hover:text-white text-sm transition-colors">Возможности</a>
                    <a href="#pricing" class="text-gray-400 hover:text-white text-sm transition-colors">Тарифы</a>
                    <a href="/login" class="text-gray-400 hover:text-white text-sm transition-colors">Войти</a>
                    <a href="/register" class="bg-white text-black px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-100 transition-colors">Начать бесплатно</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero -->
    <section class="pt-32 pb-20 px-6">
        <div class="max-w-4xl mx-auto text-center">
            <div class="inline-flex items-center px-4 py-2 rounded-full bg-gray-900 border border-gray-800 text-sm text-gray-300 mb-8">
                <span class="w-2 h-2 bg-yellow-400 rounded-full mr-2"></span>
                Новый AI-ассистент для разработчиков
            </div>
            
            <h1 class="text-5xl md:text-7xl font-bold mb-6 leading-tight">
                Проходите интервью с <span class="text-gray-400">уверенностью</span>
            </h1>
            
            <p class="text-xl text-gray-400 mb-12 max-w-2xl mx-auto leading-relaxed">
                Hintsage помогает разработчикам уверенно проходить технические интервью с помощью AI-подсказок в реальном времени
            </p>
            
            <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <a href="/register" class="bg-white text-black px-8 py-4 rounded-lg font-medium hover:bg-gray-100 transition-colors inline-flex items-center gap-2">
                    Начать бесплатно
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                </a>
                <a href="#pricing" class="border border-gray-700 text-white px-8 py-4 rounded-lg font-medium hover:border-gray-600 transition-colors">
                    Посмотреть тарифы
                </a>
            </div>
        </div>
    </section>

    <!-- Features -->
    <section id="features" class="py-20 px-6">
        <div class="max-w-6xl mx-auto">
            <div class="text-center mb-16">
                <h2 class="text-3xl md:text-4xl font-bold mb-4">Все необходимое для успешного интервью</h2>
                <p class="text-gray-400 text-lg">Мощные инструменты, которые помогут вам показать свои лучшие навыки</p>
            </div>
            
            <div class="grid md:grid-cols-3 gap-8">
                <div class="bg-gray-900 border border-gray-800 rounded-xl p-8">
                    <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-6">
                        <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">GPU Ускорение</h3>
                    <p class="text-gray-400 leading-relaxed">Whisper STT с поддержкой CUDA для мгновенного распознавания речи</p>
                </div>
                
                <div class="bg-gray-900 border border-gray-800 rounded-xl p-8">
                    <div class="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center mb-6">
                        <svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">Конфиденциальность</h3>
                    <p class="text-gray-400 leading-relaxed">Антидетект защита от скриншотов и захвата экрана</p>
                </div>
                
                <div class="bg-gray-900 border border-gray-800 rounded-xl p-8">
                    <div class="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-6">
                        <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">AI Подсказки</h3>
                    <p class="text-gray-400 leading-relaxed">GPT-4 анализирует вопросы и дает точные ответы в реальном времени</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Pricing -->
    <section id="pricing" class="py-20 px-6 bg-gray-900/50">
        <div class="max-w-6xl mx-auto">
            <div class="text-center mb-16">
                <h2 class="text-3xl md:text-4xl font-bold mb-4">Простые и прозрачные тарифы</h2>
                <p class="text-gray-400 text-lg">Выберите план, который подходит именно вам</p>
            </div>
            
            <div class="grid md:grid-cols-3 gap-8">
                <!-- Free -->
                <div class="bg-gray-900 border border-gray-800 rounded-xl p-8">
                    <h3 class="text-xl font-semibold mb-2">Free</h3>
                    <div class="mb-6">
                        <span class="text-3xl font-bold">0 ₽</span>
                        <span class="text-gray-400 ml-2">навсегда</span>
                    </div>
                    <ul class="space-y-3 mb-8">
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            Базовый STT (Vosk)
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            5 запросов в час
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            Стандартный контекст
                        </li>
                    </ul>
                    <a href="/register" class="block text-center py-3 border border-gray-700 rounded-lg hover:border-gray-600 transition-colors">
                        Начать бесплатно
                    </a>
                </div>
                
                <!-- Pro -->
                <div class="bg-gray-900 border-2 border-white rounded-xl p-8 relative">
                    <div class="absolute -top-3 left-1/2 transform -translate-x-1/2">
                        <span class="bg-white text-black px-4 py-1 rounded-full text-sm font-medium">Популярный</span>
                    </div>
                    <h3 class="text-xl font-semibold mb-2">Pro</h3>
                    <div class="mb-6">
                        <span class="text-3xl font-bold">1,499 ₽</span>
                        <span class="text-gray-400 ml-2">в месяц</span>
                    </div>
                    <ul class="space-y-3 mb-8">
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            Whisper GPU STT
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            Безлимитные запросы
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            Расширенный контекст
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            OCR скриншотов
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            Приоритетная поддержка
                        </li>
                    </ul>
                    <a href="/register" class="block text-center py-3 bg-white text-black rounded-lg hover:bg-gray-100 transition-colors">
                        Купить Pro
                    </a>
                </div>
                
                <!-- Enterprise -->
                <div class="bg-gray-900 border border-gray-800 rounded-xl p-8">
                    <h3 class="text-xl font-semibold mb-2">Enterprise</h3>
                    <div class="mb-6">
                        <span class="text-3xl font-bold">7,490 ₽</span>
                        <span class="text-gray-400 ml-2">в месяц</span>
                    </div>
                    <ul class="space-y-3 mb-8">
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            Все из Pro
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            Командный доступ
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            Кастомные интеграции
                        </li>
                        <li class="flex items-center gap-3 text-gray-300">
                            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            SLA гарантии
                        </li>
                    </ul>
                    <a href="/register" class="block text-center py-3 border border-gray-700 rounded-lg hover:border-gray-600 transition-colors">
                        Связаться с нами
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="py-20 px-6">
        <div class="max-w-4xl mx-auto text-center">
            <h2 class="text-4xl md:text-5xl font-bold mb-6">Готовы пройти интервью?</h2>
            <p class="text-xl text-gray-400 mb-10">Присоединяйтесь к разработчикам, которые уже используют Hintsage</p>
            <a href="/register" class="bg-white text-black px-8 py-4 rounded-lg font-medium hover:bg-gray-100 transition-colors inline-flex items-center gap-2">
                Начать бесплатно
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
            </a>
        </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-gray-800 py-12 px-6">
        <div class="max-w-6xl mx-auto">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div class="text-gray-400 text-sm mb-4 md:mb-0">© 2025 Hintsage. Все права защищены.</div>
                <div class="flex space-x-6">
                    <a href="/login" class="text-gray-400 hover:text-white text-sm transition-colors">Войти</a>
                    <a href="/register" class="text-gray-400 hover:text-white text-sm transition-colors">Регистрация</a>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>
"""

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход - Hintsage</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        gray: {
                            950: '#030712',
                        }
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gray-950 text-white min-h-screen flex items-center justify-center">
    <div class="max-w-md w-full mx-4">
        <!-- Logo -->
        <div class="text-center mb-8">
            <a href="/" class="text-2xl font-semibold text-white">Hintsage</a>
            <p class="text-gray-400 mt-2">Вход в систему</p>
        </div>

        <!-- Form -->
        <div class="bg-gray-900 border border-gray-800 rounded-xl p-8">
            <form method="post" class="space-y-6">
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-300 mb-2">Email</label>
                    <input
                        id="email"
                        name="email"
                        type="email"
                        required
                        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500 transition"
                        placeholder="your@email.com"
                    />
                </div>

                <div>
                    <label for="password" class="block text-sm font-medium text-gray-300 mb-2">Пароль</label>
                    <input
                        id="password"
                        name="password"
                        type="password"
                        required
                        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500 transition"
                        placeholder="••••••••"
                    />
                </div>

                <button
                    type="submit"
                    class="w-full bg-white text-black py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
                >
                    Войти
                </button>
            </form>

            <div class="mt-6 text-center">
                <p class="text-gray-400">
                    Нет аккаунта? <a href="/register" class="text-blue-400 hover:text-blue-300">Зарегистрироваться</a>
                </p>
            </div>
        </div>

        <div class="text-center mt-6">
            <a href="/" class="text-gray-400 hover:text-white transition">← Вернуться на главную</a>
        </div>
    </div>
</body>
</html>
"""

REGISTER_HTML = """
<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Регистрация - Hintsage</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        gray: {
                            950: '#030712',
                        }
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gray-950 text-white min-h-screen flex items-center justify-center">
    <div class="max-w-md w-full mx-4">
        <!-- Logo -->
        <div class="text-center mb-8">
            <a href="/" class="text-2xl font-semibold text-white">Hintsage</a>
            <p class="text-gray-400 mt-2">Создать аккаунт</p>
        </div>

        <!-- Form -->
        <div class="bg-gray-900 border border-gray-800 rounded-xl p-8">
            <form method="post" class="space-y-6">
                <div>
                    <label for="name" class="block text-sm font-medium text-gray-300 mb-2">Имя</label>
                    <input
                        id="name"
                        name="name"
                        type="text"
                        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500 transition"
                        placeholder="Ваше имя"
                    />
                </div>

                <div>
                    <label for="email" class="block text-sm font-medium text-gray-300 mb-2">Email</label>
                    <input
                        id="email"
                        name="email"
                        type="email"
                        required
                        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500 transition"
                        placeholder="your@email.com"
                    />
                </div>

                <div>
                    <label for="password" class="block text-sm font-medium text-gray-300 mb-2">Пароль</label>
                    <input
                        id="password"
                        name="password"
                        type="password"
                        required
                        minlength="8"
                        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-blue-500 transition"
                        placeholder="Минимум 8 символов"
                    />
                    <p class="text-xs text-gray-500 mt-1">Минимум 8 символов</p>
                </div>

                <button
                    type="submit"
                    class="w-full bg-white text-black py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
                >
                    Создать аккаунт
                </button>
            </form>

            <div class="mt-6 text-center">
                <p class="text-gray-400 text-sm">
                    Уже есть аккаунт? <a href="/login" class="text-blue-400 hover:text-blue-300">Войти</a>
                </p>
            </div>
        </div>

        <div class="text-center mt-6">
            <a href="/" class="text-gray-400 hover:text-white transition text-sm">← Вернуться на главную</a>
        </div>
    </div>
</body>
</html>
"""

# API функции
async def api_request(endpoint: str, method: str = "GET", data: dict = None) -> dict:
    """Выполнить запрос к Backend API"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        if method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection Error: {str(e)}"}

# Роуты
@app.get("/", response_class=HTMLResponse)
async def landing_page():
    """Главная страница"""
    return LANDING_HTML

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    """Страница входа"""
    return LOGIN_HTML

@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    """Обработка входа"""
    data = {"email": email, "password": password}
    result = await api_request("/api/v1/auth/login", "POST", data)
    
    if "error" in result:
        return HTMLResponse(f"""
        <script>
            alert('Ошибка входа: {result["error"]}');
            window.location.href = '/login';
        </script>
        """)
    
    # Сохраняем токен и редиректим
    return HTMLResponse(f"""
    <script>
        localStorage.setItem('access_token', '{result.get("access_token", "")}');
        localStorage.setItem('refresh_token', '{result.get("refresh_token", "")}');
        alert('Успешный вход!');
        window.location.href = '/dashboard';
    </script>
    """)

@app.get("/register", response_class=HTMLResponse)
async def register_page():
    """Страница регистрации"""
    return REGISTER_HTML

@app.post("/register")
async def register(
    email: str = Form(...), 
    password: str = Form(...), 
    name: str = Form("")
):
    """Обработка регистрации"""
    data = {"email": email, "password": password, "name": name}
    result = await api_request("/api/v1/auth/register", "POST", data)
    
    if "error" in result:
        return HTMLResponse(f"""
        <script>
            alert('Ошибка регистрации: {result["error"]}');
            window.location.href = '/register';
        </script>
        """)
    
    # Сохраняем токен и редиректим
    return HTMLResponse(f"""
    <script>
        localStorage.setItem('access_token', '{result.get("access_token", "")}');
        localStorage.setItem('refresh_token', '{result.get("refresh_token", "")}');
        alert('Аккаунт создан! Добро пожаловать!');
        window.location.href = '/dashboard';
    </script>
    """)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Dashboard с информацией о подписке"""
    return """
    <!DOCTYPE html>
    <html lang="ru" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - Hintsage</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {
                darkMode: 'class',
                theme: {
                    extend: {
                        colors: {
                            gray: {
                                950: '#030712',
                            }
                        }
                    }
                }
            }
        </script>
    </head>
    <body class="bg-gray-950 text-white min-h-screen">
        <!-- Navigation -->
        <nav class="border-b border-gray-800 bg-gray-950">
            <div class="max-w-7xl mx-auto px-6">
                <div class="flex items-center justify-between h-16">
                    <a href="/" class="text-xl font-semibold text-white">Hintsage</a>
                    <div class="flex items-center space-x-4">
                        <a href="/dashboard" class="text-white text-sm">Dashboard</a>
                        <a href="/pricing" class="text-gray-400 hover:text-white text-sm transition-colors">Тарифы</a>
                        <button onclick="logout()" class="text-gray-400 hover:text-white text-sm transition-colors">Выйти</button>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-7xl mx-auto px-6 py-12">
            <!-- Header -->
            <div class="mb-8">
                <h1 class="text-4xl font-bold mb-2">Личный кабинет</h1>
                <p class="text-gray-400">Управляйте своей подпиской и настройками</p>
            </div>

            <div class="grid md:grid-cols-3 gap-8">
                <!-- Main Content -->
                <div class="md:col-span-2 space-y-8">
                    <!-- Current Plan -->
                    <div class="bg-gray-900 border border-gray-800 rounded-xl p-8">
                        <div class="flex items-center justify-between mb-6">
                            <h2 class="text-2xl font-semibold">Ваш тариф</h2>
                            <span class="px-4 py-2 bg-blue-500/20 text-blue-400 rounded-lg text-sm font-semibold" id="tier-badge">
                                FREE
                            </span>
                        </div>
                        
                        <p class="text-gray-400 mb-6" id="tier-description">
                            Базовый функционал для начала работы с AI ассистентом
                        </p>

                        <!-- Features List -->
                        <div class="space-y-4 mb-8">
                            <div class="flex items-start gap-3">
                                <svg class="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                                </svg>
                                <div>
                                    <p class="text-white font-medium">Базовый STT (Vosk)</p>
                                    <p class="text-sm text-gray-500">Распознавание речи</p>
                                </div>
                            </div>
                            <div class="flex items-start gap-3">
                                <svg class="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                                </svg>
                                <div>
                                    <p class="text-white font-medium">5 запросов в час</p>
                                    <p class="text-sm text-gray-500">Лимит на AI подсказки</p>
                                </div>
                            </div>
                            <div class="flex items-start gap-3">
                                <svg class="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                                </svg>
                                <div>
                                    <p class="text-white font-medium">Стандартный контекст</p>
                                    <p class="text-sm text-gray-500">10 сообщений истории</p>
                                </div>
                            </div>
                        </div>

                        <div class="pt-6 border-t border-gray-800">
                            <a href="/pricing" class="inline-flex items-center gap-2 bg-white text-black px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition">
                                Перейти на PRO
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                                </svg>
                            </a>
                        </div>
                    </div>

                    <!-- Desktop App Section -->
                    <div class="bg-gray-900 border border-gray-800 rounded-xl p-8">
                        <h2 class="text-2xl font-semibold mb-4">Desktop приложение</h2>
                        <p class="text-gray-400 mb-6">
                            Для использования AI ассистента скачайте и запустите Desktop приложение
                        </p>
                        
                        <div class="bg-gray-800/50 border border-gray-700 rounded-lg p-6 mb-6">
                            <div class="flex items-center gap-4 mb-4">
                                <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
                                    <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                                    </svg>
                                </div>
                                <div>
                                    <p class="font-semibold text-white">Hintsage.exe</p>
                                    <p class="text-sm text-gray-500">Версия 1.0.0 • Windows 10+</p>
                                </div>
                            </div>
                            <button class="w-full bg-white text-black px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition">
                                Скачать приложение
                            </button>
                        </div>

                        <div class="space-y-3">
                            <h3 class="font-semibold text-white mb-3">Горячие клавиши:</h3>
                            <div class="flex items-center gap-3 text-sm">
                                <kbd class="px-3 py-1.5 bg-gray-800 border border-gray-700 rounded text-gray-300 font-mono">Ctrl + Shift + A</kbd>
                                <span class="text-gray-400">Захват аудио вопроса</span>
                            </div>
                            <div class="flex items-center gap-3 text-sm">
                                <kbd class="px-3 py-1.5 bg-gray-800 border border-gray-700 rounded text-gray-300 font-mono">Ctrl + Shift + S</kbd>
                                <span class="text-gray-400">Скриншот экрана</span>
                            </div>
                            <div class="flex items-center gap-3 text-sm">
                                <kbd class="px-3 py-1.5 bg-gray-800 border border-gray-700 rounded text-gray-300 font-mono">Ctrl + Shift + L</kbd>
                                <span class="text-gray-400">Авторизация</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Sidebar -->
                <div class="space-y-8">
                    <!-- Account Info -->
                    <div class="bg-gray-900 border border-gray-800 rounded-xl p-6">
                        <h3 class="font-semibold mb-4">Информация</h3>
                        <div class="space-y-3 text-sm">
                            <div>
                                <p class="text-gray-500">Email</p>
                                <p class="text-white font-medium" id="user-email">user@example.com</p>
                            </div>
                            <div>
                                <p class="text-gray-500">Подписка до</p>
                                <p class="text-white font-medium" id="subscription-end">Бессрочно</p>
                            </div>
                            <div>
                                <p class="text-gray-500">Статус</p>
                                <span class="inline-flex items-center gap-1.5 text-green-400">
                                    <span class="w-2 h-2 bg-green-400 rounded-full"></span>
                                    Активна
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Quick Stats -->
                    <div class="bg-gray-900 border border-gray-800 rounded-xl p-6">
                        <h3 class="font-semibold mb-4">Статистика</h3>
                        <div class="space-y-4">
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span class="text-gray-400">Запросов сегодня</span>
                                    <span class="text-white font-medium">0 / 5</span>
                                </div>
                                <div class="w-full bg-gray-800 rounded-full h-2">
                                    <div class="bg-blue-500 h-2 rounded-full" style="width: 0%"></div>
                                </div>
                            </div>
                            <div class="pt-4 border-t border-gray-800">
                                <p class="text-xs text-gray-500">Обновляется в реальном времени при использовании приложения</p>
                            </div>
                        </div>
                    </div>

                    <!-- Help -->
                    <div class="bg-gray-900 border border-gray-800 rounded-xl p-6">
                        <h3 class="font-semibold mb-4">Помощь</h3>
                        <div class="space-y-3 text-sm">
                            <a href="/docs/user-guide" class="block text-gray-400 hover:text-white transition">
                                📖 Руководство пользователя
                            </a>
                            <a href="/docs/faq" class="block text-gray-400 hover:text-white transition">
                                ❓ FAQ
                            </a>
                            <a href="/docs/troubleshooting" class="block text-gray-400 hover:text-white transition">
                                🔧 Решение проблем
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            function logout() {
                if (confirm('Вы уверены, что хотите выйти?')) {
                    localStorage.removeItem('jwt_token');
                    window.location.href = '/login';
                }
            }

            // Load user data from localStorage
            window.onload = function() {
                const token = localStorage.getItem('jwt_token');
                if (!token) {
                    window.location.href = '/login';
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/pricing", response_class=HTMLResponse)
async def pricing_page():
    """Страница с тарифами и покупкой"""
    return """
    <!DOCTYPE html>
    <html lang="ru" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Тарифы - Hintsage</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {
                darkMode: 'class',
                theme: {
                    extend: {
                        colors: {
                            gray: {
                                950: '#030712',
                            }
                        }
                    }
                }
            }
        </script>
    </head>
    <body class="bg-gray-950 text-white min-h-screen">
        <!-- Navigation -->
        <nav class="border-b border-gray-800 bg-gray-950">
            <div class="max-w-7xl mx-auto px-6">
                <div class="flex items-center justify-between h-16">
                    <a href="/" class="text-xl font-semibold text-white">Hintsage</a>
                    <div class="flex items-center space-x-4">
                        <a href="/dashboard" class="text-gray-400 hover:text-white text-sm transition-colors">Dashboard</a>
                        <a href="/pricing" class="text-white text-sm">Тарифы</a>
                        <a href="/login" class="text-gray-400 hover:text-white text-sm transition-colors">Войти</a>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-7xl mx-auto px-6 py-16">
            <!-- Header -->
            <div class="text-center mb-16">
                <h1 class="text-5xl font-bold mb-4">Выберите свой план</h1>
                <p class="text-xl text-gray-400 max-w-2xl mx-auto">
                    Прозрачные тарифы для разработчиков любого уровня
                </p>
            </div>

            <!-- Pricing Cards -->
            <div class="grid md:grid-cols-3 gap-8 mb-16">
                <!-- FREE -->
                <div class="bg-gray-900 border border-gray-800 rounded-xl p-8 hover:border-gray-700 transition">
                    <h3 class="text-2xl font-bold mb-2">FREE</h3>
                    <div class="mb-6">
                        <span class="text-4xl font-bold">0 ₽</span>
                        <span class="text-gray-400 ml-2">навсегда</span>
                    </div>
                    
                    <ul class="space-y-4 mb-8">
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-gray-300">Базовый STT (Vosk)</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-gray-300">5 запросов в час</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-gray-300">Стандартный контекст (10 сообщений)</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-gray-300">Базовая поддержка</span>
                        </li>
                    </ul>

                    <button class="w-full py-3 border border-gray-700 rounded-lg hover:border-gray-600 transition text-center">
                        Текущий план
                    </button>
                </div>

                <!-- PRO -->
                <div class="bg-gray-900 border-2 border-white rounded-xl p-8 relative transform scale-105">
                    <div class="absolute -top-4 left-1/2 transform -translate-x-1/2">
                        <span class="bg-white text-black px-4 py-1.5 rounded-full text-sm font-semibold">Популярный</span>
                    </div>
                    
                    <h3 class="text-2xl font-bold mb-2">PRO</h3>
                    <div class="mb-6">
                        <span class="text-4xl font-bold">1,499 ₽</span>
                        <span class="text-gray-400 ml-2">в месяц</span>
                    </div>
                    
                    <ul class="space-y-4 mb-8">
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-white mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-white"><strong>Whisper GPU STT</strong> - лучшее качество</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-white mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-white"><strong>Безлимитные</strong> запросы</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-white mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-white">Расширенный контекст (30 сообщений)</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-white mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-white">OCR скриншотов</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-white mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-white">Приоритетная поддержка</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-white mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-white">Кастомные промпты</span>
                        </li>
                    </ul>

                    <button onclick="buyPlan('pro')" class="w-full py-3 bg-white text-black rounded-lg hover:bg-gray-100 transition font-semibold">
                        Купить PRO
                    </button>
                </div>

                <!-- ENTERPRISE -->
                <div class="bg-gray-900 border border-gray-800 rounded-xl p-8 hover:border-gray-700 transition">
                    <h3 class="text-2xl font-bold mb-2">ENTERPRISE</h3>
                    <div class="mb-6">
                        <span class="text-4xl font-bold">7,490 ₽</span>
                        <span class="text-gray-400 ml-2">в месяц</span>
                    </div>
                    
                    <ul class="space-y-4 mb-8">
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-gray-300"><strong>Все из PRO</strong></span>
                        </li>
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-gray-300">Командный доступ (до 10 человек)</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-gray-300">Кастомные интеграции</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-gray-300">Выделенная поддержка 24/7</span>
                        </li>
                        <li class="flex items-start gap-3">
                            <svg class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="text-gray-300">SLA гарантии</span>
                        </li>
                    </ul>

                    <button onclick="buyPlan('enterprise')" class="w-full py-3 border border-gray-700 rounded-lg hover:border-gray-600 transition">
                        Связаться с нами
                    </button>
                </div>
            </div>

            <!-- FAQ -->
            <div class="max-w-3xl mx-auto">
                <h2 class="text-3xl font-bold mb-8 text-center">Часто задаваемые вопросы</h2>
                <div class="space-y-6">
                    <details class="bg-gray-900 border border-gray-800 rounded-lg p-6 group">
                        <summary class="cursor-pointer font-semibold text-lg flex justify-between items-center">
                            Как работает оплата?
                            <svg class="w-5 h-5 transform group-open:rotate-180 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </summary>
                        <p class="mt-4 text-gray-400">
                            Мы принимаем оплату через Банк Точка. Поддерживаются: банковские карты, СБП, Тинькофф Pay, Долями.
                            После успешной оплаты подписка активируется автоматически.
                        </p>
                    </details>

                    <details class="bg-gray-900 border border-gray-800 rounded-lg p-6 group">
                        <summary class="cursor-pointer font-semibold text-lg flex justify-between items-center">
                            Можно ли отменить подписку?
                            <svg class="w-5 h-5 transform group-open:rotate-180 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </summary>
                        <p class="mt-4 text-gray-400">
                            Да, вы можете отменить подписку в любой момент. Доступ сохранится до конца оплаченного периода.
                        </p>
                    </details>

                    <details class="bg-gray-900 border border-gray-800 rounded-lg p-6 group">
                        <summary class="cursor-pointer font-semibold text-lg flex justify-between items-center">
                            Есть ли пробный период?
                            <svg class="w-5 h-5 transform group-open:rotate-180 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </summary>
                        <p class="mt-4 text-gray-400">
                            FREE тариф доступен бессрочно без ограничений по времени. Вы можете протестировать основной функционал бесплатно.
                        </p>
                    </details>

                    <details class="bg-gray-900 border border-gray-800 rounded-lg p-6 group">
                        <summary class="cursor-pointer font-semibold text-lg flex justify-between items-center">
                            Нужна ли видеокарта NVIDIA?
                            <svg class="w-5 h-5 transform group-open:rotate-180 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </summary>
                        <p class="mt-4 text-gray-400">
                            Для FREE тарифа - нет, работает на любом ПК. Для PRO/ENTERPRISE - рекомендуется NVIDIA GPU для максимальной скорости.
                            Приложение автоматически адаптируется под ваше железо.
                        </p>
                    </details>
                </div>
            </div>
        </div>

        <script>
            async function buyPlan(plan) {
                alert(`Покупка ${plan.toUpperCase()} тарифа будет доступна после интеграции с Банк Точка API.\\n\\nСейчас в разработке! 🚀`);
                
                // В production здесь будет:
                // 1. Запрос к Backend API для создания платежа
                // 2. Редирект на страницу оплаты Банк Точка
                // 3. После оплаты - webhook активирует подписку
            }
        </script>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Проверка здоровья Frontend"""
    return {"status": "healthy", "service": "frontend_python", "version": "1.0.0"}

if __name__ == "__main__":
    print("🚀 Запуск Hintsage Python Frontend...")
    print("📱 Откройте: http://localhost:3001")
    print("🔗 Backend API: http://localhost:8000")
    
    uvicorn.run(
        "frontend_python:app",
        host="0.0.0.0",
        port=3001,
        reload=True,
        log_level="info"
    )
