"""
Syntax Highlighter - [МЫСЛЕТЕ + ЛИЧЬ]
Подсветка синтаксиса кода, формул, UML
"""

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
import markdown
from typing import Optional
from loguru import logger
import re


class SyntaxHighlighter:
    """
    Подсветка синтаксиса
    Архетипы:
    - МЫСЛЕТЕ: разбор кода
    - ЛИЧЬ: визуализация
    - ВЕДИ: форматирование
    """
    
    def __init__(
        self,
        theme: str = "monokai",
        enable_code_blocks: bool = True,
        enable_math: bool = True,
        enable_uml: bool = False
    ):
        """
        Инициализация подсветчика
        
        Args:
            theme: Тема подсветки (monokai, github, vs, solarized)
            enable_code_blocks: Включить подсветку кода
            enable_math: Включить формулы
            enable_uml: Включить UML диаграммы
        """
        self.theme = theme
        self.enable_code_blocks = enable_code_blocks
        self.enable_math = enable_math
        self.enable_uml = enable_uml
        
        # Pygments formatter
        self.formatter = HtmlFormatter(style=self.theme, full=False)
        
        logger.info(f"[OK] SyntaxHighlighter инициализирован (тема: {theme})")
    
    def highlight_code(self, code: str, language: Optional[str] = None) -> str:
        """
        [МЫСЛЕТЕ + ЛИЧЬ] - Подсветить код
        
        Args:
            code: Код для подсветки
            language: Язык программирования (python, javascript, etc.) или None для автоопределения
        
        Returns:
            HTML с подсвеченным кодом
        """
        if not self.enable_code_blocks:
            return f"<pre><code>{code}</code></pre>"
        
        try:
            # Определяем язык
            if language:
                lexer = get_lexer_by_name(language, stripall=True)
            else:
                lexer = guess_lexer(code)
            
            # Подсвечиваем
            highlighted = highlight(code, lexer, self.formatter)
            
            # Добавляем обертку
            result = f'<div class="code-block">{highlighted}</div>'
            
            logger.debug(f"Код подсвечен (язык: {lexer.name})")
            return result
        
        except Exception as e:
            logger.error(f"Ошибка подсветки кода: {e}")
            return f"<pre><code>{code}</code></pre>"
    
    def process_markdown(self, text: str) -> str:
        """
        [МЫСЛЕТЕ + ЛИЧЬ] - Обработать Markdown с подсветкой кода
        
        Args:
            text: Markdown текст
        
        Returns:
            HTML
        """
        try:
            # Обрабатываем блоки кода
            if self.enable_code_blocks:
                text = self._process_code_blocks(text)
            
            # Конвертируем Markdown в HTML
            html = markdown.markdown(
                text,
                extensions=['extra', 'codehilite', 'fenced_code']
            )
            
            return html
        
        except Exception as e:
            logger.error(f"Ошибка обработки Markdown: {e}")
            return text
    
    def _process_code_blocks(self, text: str) -> str:
        """
        [МЫСЛЕТЕ] - Обработать блоки кода в тексте
        
        Args:
            text: Текст с кодом
        
        Returns:
            Текст с подсвеченным кодом
        """
        # Regex для ```language\ncode\n```
        pattern = r'```(\w+)?\n(.*?)```'
        
        def replace_code_block(match):
            language = match.group(1)
            code = match.group(2)
            return self.highlight_code(code, language)
        
        result = re.sub(pattern, replace_code_block, text, flags=re.DOTALL)
        return result
    
    def format_math(self, formula: str) -> str:
        """
        [ЛИЧЬ] - Форматировать математическую формулу
        
        Args:
            formula: LaTeX формула
        
        Returns:
            HTML с формулой
        """
        if not self.enable_math:
            return formula
        
        # Простое обрамление для MathJax/KaTeX
        return f'<span class="math">\\({formula}\\)</span>'
    
    def get_css(self) -> str:
        """
        [ЛИЧЬ] - Получить CSS для подсветки
        
        Returns:
            CSS код
        """
        # Базовый CSS от Pygments
        pygments_css = self.formatter.get_style_defs('.highlight')
        
        # Дополнительные стили
        custom_css = """
        .code-block {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .math {
            font-family: 'Cambria Math', 'Times New Roman', serif;
            font-style: italic;
        }
        """
        
        return f"{pygments_css}\n{custom_css}"
    
    def format_answer(self, answer: str) -> str:
        """
        [МЫСЛЕТЕ + ЛИЧЬ] - Полное форматирование ответа
        
        Args:
            answer: Исходный ответ от LLM
        
        Returns:
            Форматированный HTML
        """
        # Обрабатываем Markdown + код
        html = self.process_markdown(answer)
        
        # Обрабатываем математику (если включено)
        if self.enable_math:
            html = self._process_math_blocks(html)
        
        return html
    
    def _process_math_blocks(self, text: str) -> str:
        """
        [МЫСЛЕТЕ] - Обработать математические блоки
        
        Args:
            text: Текст с формулами
        
        Returns:
            Текст с обработанными формулами
        """
        # Inline math: $formula$
        text = re.sub(r'\$([^\$]+)\$', lambda m: self.format_math(m.group(1)), text)
        
        # Block math: $$formula$$
        text = re.sub(
            r'\$\$([^\$]+)\$\$',
            lambda m: f'<div class="math-block">\\[{m.group(1)}\\]</div>',
            text
        )
        
        return text


