"""
Auth Manager - [ШТОР + АЗ]
Управление авторизацией через браузер и JWT токены
"""

import webbrowser
import json
from typing import Optional, Dict, List
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from threading import Thread
from loguru import logger
import jwt
from datetime import datetime


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler для получения callback с JWT токеном"""
    
    auth_manager: Optional['AuthManager'] = None
    
    def do_GET(self):
        """Обработка GET запроса с токеном"""
        try:
            parsed_path = urlparse(self.path)
            
            if parsed_path.path == '/callback':
                # Получаем токен из query параметров
                params = parse_qs(parsed_path.query)
                token = params.get('token', [None])[0]
                
                if token and self.auth_manager:
                    self.auth_manager._handle_callback(token)
                    
                    # Отправляем успешный ответ
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    
                    html = """
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <title>Hintsage - Авторизация успешна</title>
                        <style>
                            body {
                                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                height: 100vh;
                                margin: 0;
                            }
                            .container {
                                background: white;
                                padding: 3rem;
                                border-radius: 1rem;
                                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                                text-align: center;
                            }
                            h1 { color: #667eea; margin-bottom: 1rem; }
                            p { color: #666; font-size: 1.1rem; }
                            .checkmark {
                                width: 80px;
                                height: 80px;
                                border-radius: 50%;
                                display: block;
                                stroke-width: 2;
                                stroke: #4bb543;
                                stroke-miterlimit: 10;
                                margin: 10% auto;
                                box-shadow: inset 0px 0px 0px #4bb543;
                                animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
                            }
                            @keyframes scale {
                                0%, 100% { transform: none; }
                                50% { transform: scale3d(1.1, 1.1, 1); }
                            }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                                <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
                                <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                            </svg>
                            <h1>✅ Авторизация успешна!</h1>
                            <p>Вы можете закрыть это окно и вернуться в приложение.</p>
                        </div>
                        <script>
                            setTimeout(() => window.close(), 3000);
                        </script>
                    </body>
                    </html>
                    """
                    self.wfile.write(html.encode())
                else:
                    self.send_error(400, "Token not provided")
            else:
                self.send_error(404)
                
        except Exception as e:
            logger.error(f"Error in callback handler: {e}")
            self.send_error(500)
    
    def log_message(self, format, *args):
        """Отключаем логирование HTTP сервера"""
        pass


class AuthManager:
    """
    Менеджер авторизации через браузер
    Архетипы: ШТОР (безопасность) + АЗ (управление доступом)
    """
    
    def __init__(self, backend_url: str = "http://localhost:8000", frontend_url: str = "http://localhost:3000"):
        self.backend_url = backend_url
        self.frontend_url = frontend_url
        self.callback_port = 8765
        self.jwt_token: Optional[str] = None
        self.user_data: Optional[Dict] = None
        self.subscription_tier: str = "free"
        self.features: List[str] = []
        
        # HTTP сервер для callback
        self._server: Optional[HTTPServer] = None
        self._server_thread: Optional[Thread] = None
        
    def login(self) -> bool:
        """
        Начать процесс авторизации через браузер
        
        Returns:
            True если авторизация успешна
        """
        try:
            logger.info("🔐 Начинаем процесс авторизации...")
            
            # Запускаем локальный HTTP сервер для callback
            self._start_callback_server()
            
            # Формируем URL для авторизации
            callback_url = f"http://localhost:{self.callback_port}/callback"
            auth_url = f"{self.frontend_url}/login?callback={callback_url}"
            
            logger.info(f"🌐 Открываем браузер: {auth_url}")
            
            # Открываем браузер
            webbrowser.open(auth_url)
            
            logger.info("⏳ Ожидаем авторизации в браузере...")
            logger.info("Пожалуйста, войдите в систему через открывшуюся страницу")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка при запуске авторизации: {e}")
            return False
    
    def _start_callback_server(self):
        """Запустить HTTP сервер для получения callback"""
        try:
            # Устанавливаем ссылку на AuthManager в handler
            CallbackHandler.auth_manager = self
            
            # Создаем сервер
            self._server = HTTPServer(('localhost', self.callback_port), CallbackHandler)
            
            # Запускаем в отдельном потоке
            self._server_thread = Thread(target=self._server.serve_forever, daemon=True)
            self._server_thread.start()
            
            logger.info(f"✅ Callback сервер запущен на порту {self.callback_port}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка запуска callback сервера: {e}")
            raise
    
    def _handle_callback(self, token: str):
        """
        Обработать callback с JWT токеном
        
        Args:
            token: JWT токен от backend
        """
        try:
            logger.info("🔑 Получен JWT токен")
            
            # Сохраняем токен
            self.jwt_token = token
            
            # Декодируем токен (без проверки подписи для извлечения данных)
            payload = jwt.decode(token, options={"verify_signature": False})
            
            # Извлекаем данные
            self.user_data = {
                "id": payload.get("sub"),
                "email": payload.get("email"),
                "name": payload.get("name"),
                "email_verified": payload.get("email_verified", False)
            }
            
            self.subscription_tier = payload.get("tier", "free")
            self.features = payload.get("features", [])
            
            logger.info(f"✅ Авторизация успешна!")
            logger.info(f"   Email: {self.user_data['email']}")
            logger.info(f"   Tier: {self.subscription_tier}")
            logger.info(f"   Features: {len(self.features)} шт")
            
            # Останавливаем сервер
            self._stop_callback_server()
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки токена: {e}")
    
    def _stop_callback_server(self):
        """Остановить callback сервер"""
        if self._server:
            self._server.shutdown()
            self._server = None
            logger.info("🛑 Callback сервер остановлен")
    
    def is_authenticated(self) -> bool:
        """Проверить, авторизован ли пользователь"""
        return self.jwt_token is not None
    
    def get_token(self) -> Optional[str]:
        """Получить JWT токен"""
        return self.jwt_token
    
    def get_user_data(self) -> Optional[Dict]:
        """Получить данные пользователя"""
        return self.user_data
    
    def get_subscription_tier(self) -> str:
        """Получить тариф подписки"""
        return self.subscription_tier
    
    def get_features(self) -> List[str]:
        """Получить список доступных фич"""
        return self.features
    
    def has_feature(self, feature: str) -> bool:
        """
        Проверить доступность фичи
        
        Args:
            feature: Название фичи (например, "advanced_stt")
        
        Returns:
            True если фича доступна
        """
        return feature in self.features
    
    def logout(self):
        """Выйти из аккаунта"""
        self.jwt_token = None
        self.user_data = None
        self.subscription_tier = "free"
        self.features = []
        logger.info("👋 Вышли из аккаунта")
    
    def __del__(self):
        """Cleanup при удалении объекта"""
        self._stop_callback_server()

