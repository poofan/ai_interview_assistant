"""
Speech-to-Text Module
Архетипы: [МЫСЛЕТЕ + ВЕДИ]
Функции: Преобразование речи в текст (Vosk, Whisper)
"""

from .stt_engine import STTEngine, VoskSTT, WhisperSTT, STTManager

__all__ = ["STTEngine", "VoskSTT", "WhisperSTT", "STTManager"]

