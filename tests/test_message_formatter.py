"""Тесты для модуля message_formatter"""

from datetime import datetime

from src.message_formatter import MessageFormatter
from src.models import ConversationContext, LLMResponse, UserMessage


def test_format_empty_context():
    """Тест: Форматирование при отсутствии контекста"""
    formatter = MessageFormatter()
    messages = formatter.format_for_llm(None, "Default prompt")

    assert len(messages) == 1
    assert messages[0] == {"role": "system", "content": "Default prompt"}


def test_format_with_one_message():
    """Тест: Форматирование с одним сообщением"""
    context = ConversationContext(
        user_id=123,
        messages=[UserMessage(123, "Hello", datetime.now())],
        responses=[],
        system_prompt="System prompt",
    )

    formatter = MessageFormatter()
    messages = formatter.format_for_llm(context, "Default")

    assert len(messages) == 2
    assert messages[0] == {"role": "system", "content": "System prompt"}
    assert messages[1] == {"role": "user", "content": "Hello"}


def test_format_with_full_conversation():
    """Тест: Форматирование полного диалога"""
    context = ConversationContext(
        user_id=123,
        messages=[
            UserMessage(123, "Hello", datetime.now()),
            UserMessage(123, "How are you?", datetime.now()),
        ],
        responses=[
            LLMResponse("Hi!", datetime.now(), "gpt-3.5"),
            LLMResponse("I'm fine", datetime.now(), "gpt-3.5"),
        ],
        system_prompt="System prompt",
    )

    formatter = MessageFormatter()
    messages = formatter.format_for_llm(context, "Default")

    assert len(messages) == 5
    assert messages[0]["role"] == "system"
    assert messages[1] == {"role": "user", "content": "Hello"}
    assert messages[2] == {"role": "assistant", "content": "Hi!"}
    assert messages[3] == {"role": "user", "content": "How are you?"}
    assert messages[4] == {"role": "assistant", "content": "I'm fine"}

