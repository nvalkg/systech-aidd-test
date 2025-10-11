"""Модели данных для диалогов"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserMessage:
    """Сообщение пользователя"""

    user_id: int
    text: str
    timestamp: datetime


@dataclass
class LLMResponse:
    """Ответ LLM"""

    content: str
    timestamp: datetime
    model_used: str


@dataclass
class ConversationContext:
    """Контекст диалога"""

    user_id: int
    messages: list[UserMessage]
    responses: list[LLMResponse]
    system_prompt: str
