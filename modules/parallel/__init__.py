"""
Parallel Processing Module
Модуль параллельной обработки запросов
"""

from .request_queue import RequestQueue, RequestTask

__all__ = ["RequestQueue", "RequestTask"]

