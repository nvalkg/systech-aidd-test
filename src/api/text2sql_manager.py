"""Менеджер для text2sql запросов в admin режиме"""

import logging
import re

from sqlalchemy.ext.asyncio import AsyncEngine

from ..llm_client import LLMClient

logger = logging.getLogger(__name__)


class Text2SQLManager:
    """
    Менеджер для обработки запросов в admin режиме с text2sql

    Pipeline:
    1. Вопрос пользователя → LLM генерирует SQL
    2. Валидация SQL (безопасность)
    3. Выполнение SQL запроса
    4. Результат → LLM форматирует ответ
    """

    def __init__(self, llm_client: LLMClient, engine: AsyncEngine, text2sql_prompt: str):
        """
        Инициализация Text2SQL менеджера

        Args:
            llm_client: Клиент для работы с LLM
            engine: Асинхронный движок SQLAlchemy
            text2sql_prompt: Системный промпт для генерации SQL
        """
        self.llm_client = llm_client
        self.engine = engine
        self.text2sql_prompt = text2sql_prompt
        logger.info("Text2SQLManager инициализирован")

    async def process_query(self, question: str) -> tuple[str, str]:
        """
        Обработать вопрос пользователя через text2sql pipeline

        Args:
            question: Вопрос на естественном языке

        Returns:
            Tuple (ответ на естественном языке, SQL запрос)
        """
        try:
            # Шаг 1: Генерация SQL из вопроса
            sql_query = await self._generate_sql(question)

            # Шаг 2: Валидация SQL
            if not self._is_safe_sql(sql_query):
                logger.warning(f"Небезопасный SQL запрос: {sql_query[:100]}")
                return (
                    "Извините, запрос не может быть выполнен по соображениям безопасности. "
                    "Поддерживаются только SELECT запросы к таблицам диалогов.",
                    sql_query,
                )

            # Шаг 3: Выполнение SQL
            result = await self._execute_sql(sql_query)

            # Шаг 4: Форматирование ответа через LLM
            answer = await self._format_answer(question, sql_query, result)

            return (answer, sql_query)

        except Exception as e:
            logger.error(f"Ошибка при обработке text2sql запроса: {e}")
            error_answer = (
                f"Извините, произошла ошибка при обработке запроса: {str(e)}. "
                "Попробуйте переформулировать вопрос."
            )
            return (error_answer, "-- Ошибка генерации SQL")

    async def _generate_sql(self, question: str) -> str:
        """
        Генерация SQL запроса из вопроса через LLM

        Args:
            question: Вопрос на естественном языке

        Returns:
            SQL запрос
        """
        messages = [
            {"role": "system", "content": self.text2sql_prompt},
            {
                "role": "user",
                "content": f"Сгенерируй SQL запрос для следующего вопроса:\n\n{question}",
            },
        ]

        response = await self.llm_client.get_response(messages)

        # Извлекаем SQL из блока кода
        sql_query = self._extract_sql_from_response(response)

        logger.info(f"Сгенерирован SQL для вопроса: {question[:50]}...")
        logger.debug(f"SQL запрос: {sql_query}")

        return sql_query

    def _extract_sql_from_response(self, response: str) -> str:
        """
        Извлечь SQL код из ответа LLM

        Args:
            response: Ответ LLM

        Returns:
            SQL запрос без обертки
        """
        # Ищем SQL в блоках кода ```sql ... ```
        match = re.search(r"```sql\s+(.*?)\s+```", response, re.DOTALL | re.IGNORECASE)
        if match:
            sql = match.group(1).strip()
        else:
            # Если нет блока кода, пробуем найти SELECT
            match = re.search(r"(SELECT\s+.*?;)", response, re.DOTALL | re.IGNORECASE)
            if match:
                sql = match.group(1).strip()
            else:
                # Возвращаем весь ответ как есть
                sql = response.strip()

        # Удаляем комментарии для безопасности (но сохраняем начальный комментарий)
        lines = sql.split("\n")
        cleaned_lines = []
        for line in lines:
            # Убираем inline комментарии в середине запроса
            if "--" in line:
                # Оставляем только если это первая строка (описание)
                if not cleaned_lines or not line.strip().startswith("--"):
                    line = line.split("--")[0]
            cleaned_lines.append(line)

        sql = "\n".join(cleaned_lines).strip()

        return sql

    def _is_safe_sql(self, sql_query: str) -> bool:
        """
        Проверка SQL запроса на безопасность

        Args:
            sql_query: SQL запрос для проверки

        Returns:
            True если запрос безопасен, False иначе
        """
        sql_upper = sql_query.upper()

        # Список запрещенных операций
        forbidden_keywords = [
            "INSERT",
            "UPDATE",
            "DELETE",
            "DROP",
            "CREATE",
            "ALTER",
            "TRUNCATE",
            "EXEC",
            "EXECUTE",
            "GRANT",
            "REVOKE",
        ]

        # Проверяем на запрещенные ключевые слова
        for keyword in forbidden_keywords:
            if re.search(rf"\b{keyword}\b", sql_upper):
                logger.warning(f"Обнаружено запрещенное ключевое слово: {keyword}")
                return False

        # Проверяем, что запрос начинается с SELECT
        if not re.match(r"^\s*(--.*\n)*\s*SELECT\b", sql_upper):
            logger.warning("SQL запрос не начинается с SELECT")
            return False

        # Проверяем на SQL injection паттерны
        dangerous_patterns = [
            r";.*SELECT",  # Множественные запросы
            r";\s*INSERT",
            r";\s*UPDATE",
            r";\s*DELETE",
            r";\s*DROP",
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, sql_upper):
                logger.warning(f"Обнаружен опасный паттерн: {pattern}")
                return False

        return True

    async def _execute_sql(self, sql_query: str) -> list[dict]:
        """
        Выполнить SQL запрос

        Args:
            sql_query: SQL запрос

        Returns:
            Результат выполнения как список словарей
        """
        async with self.engine.begin() as conn:
            result = await conn.execute(text(sql_query))
            rows = result.fetchall()

            # Преобразуем в список словарей
            if rows:
                columns = result.keys()
                data = [dict(zip(columns, row, strict=False)) for row in rows]
            else:
                data = []

        logger.info(f"SQL запрос выполнен успешно, получено {len(data)} строк")
        return data

    async def _format_answer(self, question: str, sql_query: str, result: list[dict]) -> str:
        """
        Форматировать ответ на естественном языке через LLM

        Args:
            question: Исходный вопрос пользователя
            sql_query: Выполненный SQL запрос
            result: Результат выполнения SQL

        Returns:
            Ответ на естественном языке
        """
        # Ограничиваем размер результата для контекста LLM
        result_preview = result[:50] if len(result) > 50 else result
        result_text = str(result_preview)
        if len(result) > 50:
            result_text += f"\n... (показаны первые 50 из {len(result)} строк)"

        messages = [
            {
                "role": "system",
                "content": "Ты - помощник по аналитике диалогов. Твоя задача - представить результаты SQL запросов в понятном и дружелюбном виде на русском языке.",
            },
            {
                "role": "user",
                "content": f"""Вопрос пользователя: {question}

SQL запрос, который был выполнен:
```sql
{sql_query}
```

Результат выполнения:
{result_text}

Пожалуйста, сформулируй ответ на естественном языке, объясни результаты просто и понятно.""",
            },
        ]

        answer = await self.llm_client.get_response(messages)

        logger.info(f"Сформирован ответ на вопрос: {question[:50]}...")

        return answer


# Нужно импортировать text для выполнения сырых SQL запросов
from sqlalchemy import text  # noqa: E402
