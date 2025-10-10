"""
Parallel Processing Utils
Утилиты для параллельной обработки
"""


def truncate_question(question: str, max_length: int = 100) -> str:
    """
    [СЛОВО + ЛИЧЬ] - Сократить длинный вопрос для отображения
    
    Args:
        question: Полный текст вопроса
        max_length: Максимальная длина
    
    Returns:
        Сокращенный вопрос
    
    Examples:
        >>> truncate_question("Что такое HashMap?", 100)
        "Что такое HashMap?"
        
        >>> truncate_question("Очень длинный вопрос про HashMap и его внутреннюю реализацию...", 50)
        "Очень длинный вопрос про HashMap и его внутр..."
    """
    if len(question) <= max_length:
        return question
    
    # Сокращаем, сохраняя смысл
    truncated = question[:max_length - 3].rstrip()
    
    # Пытаемся найти последнюю полную фразу/слово
    last_space = truncated.rfind(' ')
    if last_space > max_length // 2:  # Если нашли пробел в разумном месте
        truncated = truncated[:last_space]
    
    return truncated + "..."


def format_answer_with_question(
    request_number: int,
    question: str,
    answer: str,
    show_question: bool = True,
    question_max_length: int = 100
) -> str:
    """
    [ЛИЧЬ + СЛОВО] - Форматировать ответ с вопросом
    
    Args:
        request_number: Номер запроса [Q1], [Q2]...
        question: Полный текст вопроса
        answer: Текст ответа
        show_question: Показывать ли вопрос
        question_max_length: Макс длина вопроса
    
    Returns:
        Отформатированный текст
    
    Examples:
        >>> format_answer_with_question(1, "Что такое HashMap?", "HashMap - это хеш-таблица...")
        "[Q1] 📝 Что такое HashMap?\\n\\n💡 HashMap - это хеш-таблица..."
    """
    if show_question:
        # Сокращаем вопрос если нужно
        display_question = truncate_question(question, question_max_length)
        
        return f"[Q{request_number}] 📝 {display_question}\n\n💡 {answer}"
    else:
        return f"[Q{request_number}] {answer}"


def get_stage_emoji(stage: str) -> str:
    """
    Получить emoji для этапа обработки
    
    Args:
        stage: Название этапа (STT, LLM, etc.)
    
    Returns:
        Emoji
    """
    stage_emojis = {
        "STT": "🎙️",
        "LLM": "🤖",
        "OCR": "👁️",
        "CONTEXT": "📚",
        "ERROR": "❌",
        "DONE": "✅"
    }
    
    return stage_emojis.get(stage.upper(), "🔄")

