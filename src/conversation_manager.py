"""Управление контекстом диалога"""

import logging

from .db_history_storage import DatabaseHistoryStorage
from .history_storage import HistoryStorage
from .llm_client import LLMClient
from .message_formatter import MessageFormatter
from .prompt_loader import PromptLoader

logger = logging.getLogger(__name__)


class ConversationManager:
    """Оркестратор диалога - координирует взаимодействие компонентов"""

    def __init__(
        self,
        llm_client: LLMClient,
        system_prompt: str,
        storage: HistoryStorage | DatabaseHistoryStorage | None = None,
        max_history: int = 10,
    ) -> None:
        """
        Инициализация менеджера диалога

        Args:
            llm_client: Клиент для работы с LLM
            system_prompt: Системный промпт для LLM
            storage: Хранилище истории (HistoryStorage или DatabaseHistoryStorage)
            max_history: Максимальное количество сообщений в истории (если storage не передан)
        """
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self.storage = storage if storage is not None else HistoryStorage(max_history)
        self.formatter = MessageFormatter()
        self.prompt_loader = PromptLoader(prompt_text=system_prompt)

        storage_type = type(self.storage).__name__
        logger.info(f"ConversationManager инициализирован (storage={storage_type})")

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
        if isinstance(self.storage, DatabaseHistoryStorage):
            await self.storage.add_message(user_id, text, self.system_prompt)
        else:
            self.storage.add_message(user_id, text, self.system_prompt)

        # Получаем контекст и форматируем для LLM
        if isinstance(self.storage, DatabaseHistoryStorage):
            context = await self.storage.get_context(user_id)
        else:
            context = self.storage.get_context(user_id)

        messages = self.formatter.format_for_llm(context, self.system_prompt)

        # Получаем ответ от LLM
        response = await self.llm_client.get_response(messages)

        # Сохраняем ответ
        if isinstance(self.storage, DatabaseHistoryStorage):
            await self.storage.add_response(user_id, response, self.llm_client.model)
        else:
            self.storage.add_response(user_id, response, self.llm_client.model)

        return response

    async def clear_history(self, user_id: int) -> None:
        """Очистить историю диалога пользователя"""
        if isinstance(self.storage, DatabaseHistoryStorage):
            await self.storage.clear(user_id)
        else:
            self.storage.clear(user_id)

    def get_role_description(self) -> str:
        """
        Получить описание роли бота для команды /role

        Returns:
            str: Форматированное описание роли
        """
        return self.prompt_loader.get_role_description()
