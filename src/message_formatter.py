"""Форматирование сообщений для LLM API"""

import logging

from .models import ConversationContext

logger = logging.getLogger(__name__)


class MessageFormatter:
    """Форматирование сообщений для LLM API"""

    @staticmethod
    def format_for_llm(
        context: ConversationContext | None, system_prompt: str
    ) -> list[dict[str, str]]:
        """
        Форматировать контекст для LLM API

        Args:
            context: Контекст диалога
            system_prompt: Системный промпт по умолчанию

        Returns:
            Список сообщений в формате OpenAI API
        """
        # Если контекста нет, возвращаем только system prompt
        if context is None:
            return [{"role": "system", "content": system_prompt}]

        messages: list[dict[str, str]] = [{"role": "system", "content": context.system_prompt}]

        # Чередуем user и assistant сообщения
        for i in range(min(len(context.messages), len(context.responses))):
            messages.append({"role": "user", "content": context.messages[i].text})
            messages.append({"role": "assistant", "content": context.responses[i].content})

        # Если есть непарное сообщение пользователя
        if len(context.messages) > len(context.responses):
            messages.append({"role": "user", "content": context.messages[-1].text})

        logger.debug(f"Отформатировано {len(messages)} сообщений для LLM")
        return messages
