"""
Тест определения профиля и улучшения вопросов
"""

from modules.prompt_templates import PromptManager, InterviewProfile
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="<level>{level: <8}</level> | <cyan>{message}</cyan>")

def test_question(question: str, pm: PromptManager):
    """Тест одного вопроса"""
    print("\n" + "="*60)
    print(f"ВОПРОС: {question}")
    print("="*60)
    
    # Определяем тип
    detected = pm.detect_question_type(question)
    print(f"ОПРЕДЕЛЕН ТИП: {detected.value}")
    
    # Улучшаем
    enhanced = pm.enhance_question(question, detected)
    print(f"\nУЛУЧШЕННЫЙ ВОПРОС:\n{enhanced}")
    
    # Промпт
    system_prompt = pm.get_system_prompt(detected)
    print(f"\nСИСТЕМНЫЙ ПРОМПТ (первые 200 символов):\n{system_prompt[:200]}...")

def main():
    pm = PromptManager(
        default_profile=InterviewProfile.ALGORITHMS,
        programming_language="Java",
        auto_detect_language=True
    )
    
    print("\n" + "=== ТЕСТ ОПРЕДЕЛЕНИЯ ПРОФИЛЕЙ ===" + "\n")
    
    # Теоретические вопросы
    test_question("Дайте краткую характеристику immutable object. Зачем они нужны?", pm)
    test_question("Что такое полиморфизм?", pm)
    test_question("В чем разница между interface и abstract class?", pm)
    
    # Алгоритмические вопросы
    test_question("Напиши функцию для binary search", pm)
    test_question("Реализуй quicksort", pm)
    
    # Code review
    test_question("Что не так с этим кодом?", pm)
    
    # System design
    test_question("Спроектируй систему для обработки 1M запросов в секунду", pm)

if __name__ == "__main__":
    main()

