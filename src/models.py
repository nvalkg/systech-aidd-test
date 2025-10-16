"""Модели данных для диалогов"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UserMessage:
    """Сообщение пользователя"""

    user_id: int
    text: str
    timestamp: datetime
    content_length: int = field(init=False)
    id: int | None = None
    is_deleted: bool = False

    def __post_init__(self) -> None:
        """Вычисляем длину контента после инициализации"""
        self.content_length = len(self.text)


@dataclass
class LLMResponse:
    """Ответ LLM"""

    content: str
    timestamp: datetime
    model_used: str
    content_length: int = field(init=False)
    id: int | None = None
    is_deleted: bool = False

    def __post_init__(self) -> None:
        """Вычисляем длину контента после инициализации"""
        self.content_length = len(self.content)


@dataclass
class ConversationContext:
    """Контекст диалога"""

    user_id: int
    messages: list[UserMessage]
    responses: list[LLMResponse]
    system_prompt: str
