"""Управление контекстом диалога"""

import logging

from .history_storage import HistoryStorage
from .llm_client import LLMClient
from .message_formatter import MessageFormatter

logger = logging.getLogger(__name__)


class ConversationManager:
    """Оркестратор диалога - координирует взаимодействие компонентов"""

    def __init__(self, llm_client: LLMClient, system_prompt: str, max_history: int = 10) -> None:
        """
        Инициализация менеджера диалога

        Args:
            llm_client: Клиент для работы с LLM
            system_prompt: Системный промпт для LLM
            max_history: Максимальное количество сообщений в истории
        """
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self.storage = HistoryStorage(max_history)
        self.formatter = MessageFormatter()

        logger.info(f"ConversationManager инициализирован (max_history={max_history})")

    async def process_message(self, user_id: int, text: str) -> str:
        """
        Обработать сообщение пользователя и получить ответ

        Args:
            user_id: ID пользователя
            text: Текст сообщения

        Returns:
            Ответ от LLM
        """
        # Сохраняем сообщение пользователя
        self.storage.add_message(user_id, text, self.system_prompt)

        # Получаем контекст и форматируем для LLM
        context = self.storage.get_context(user_id)
        messages = self.formatter.format_for_llm(context, self.system_prompt)

        # Получаем ответ от LLM
        response = await self.llm_client.get_response(messages)

        # Сохраняем ответ
        self.storage.add_response(user_id, response, self.llm_client.model)

        return response

    def clear_history(self, user_id: int) -> None:
        """Очистить историю диалога пользователя"""
        self.storage.clear(user_id)
