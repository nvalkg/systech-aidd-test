"""Хранение истории диалогов"""

import logging
from datetime import datetime

from .models import ConversationContext, LLMResponse, UserMessage

logger = logging.getLogger(__name__)


class HistoryStorage:
    """Хранилище истории диалогов"""

    def __init__(self, max_history: int = 10) -> None:
        """
        Инициализация хранилища

        Args:
            max_history: Максимальное количество сообщений в истории
        """
        self.max_history = max_history
        self.contexts: dict[int, ConversationContext] = {}
        logger.info(f"HistoryStorage инициализирован (max_history={max_history})")

    def get_or_create_context(self, user_id: int, system_prompt: str) -> ConversationContext:
        """Получить или создать контекст для пользователя"""
        if user_id not in self.contexts:
            self.contexts[user_id] = ConversationContext(
                user_id=user_id,
                messages=[],
                responses=[],
                system_prompt=system_prompt,
            )
            logger.debug(f"Создан новый контекст для user {user_id}")
        return self.contexts[user_id]

    def add_message(self, user_id: int, text: str, system_prompt: str) -> None:
        """Добавить сообщение пользователя"""
        context = self.get_or_create_context(user_id, system_prompt)
        message = UserMessage(user_id=user_id, text=text, timestamp=datetime.now())
        context.messages.append(message)
        self._trim_history(user_id)
        logger.info(f"Добавлено сообщение от user {user_id} ({len(text)} символов)")

    def add_response(self, user_id: int, content: str, model: str) -> None:
        """Добавить ответ LLM"""
        if user_id not in self.contexts:
            logger.warning(f"Попытка добавить ответ для несуществующего user {user_id}")
            return

        response = LLMResponse(content=content, timestamp=datetime.now(), model_used=model)
        self.contexts[user_id].responses.append(response)
        self._trim_history(user_id)
        logger.info(f"Добавлен ответ для user {user_id} ({len(content)} символов)")

    def get_context(self, user_id: int) -> ConversationContext | None:
        """Получить контекст пользователя"""
        return self.contexts.get(user_id)

    def clear(self, user_id: int) -> None:
        """Очистить историю пользователя"""
        if user_id in self.contexts:
            del self.contexts[user_id]
            logger.info(f"История для user {user_id} очищена")

    def _trim_history(self, user_id: int) -> None:
        """Ограничить историю до max_history"""
        context = self.contexts[user_id]
        # Синхронизируем обрезку messages и responses
        max_len = max(len(context.messages), len(context.responses))
        if max_len > self.max_history:
            context.messages = context.messages[-self.max_history :]
            context.responses = context.responses[-self.max_history :]
            logger.debug(f"История user {user_id} обрезана до {self.max_history} сообщений")
