"""Тесты для модуля conversation_manager"""

import pytest
from unittest.mock import AsyncMock

from src.conversation_manager import ConversationManager


@pytest.fixture
def mock_llm_client():
    """Мок LLMClient"""
    client = AsyncMock()
    client.model = "test-model"
    client.get_response = AsyncMock(return_value="Test response")
    return client


@pytest.mark.asyncio
async def test_process_message(mock_llm_client):
    """Тест: Обработка сообщения"""
    manager = ConversationManager(mock_llm_client, "System prompt", max_history=10)

    response = await manager.process_message(123, "Hello")

    assert response == "Test response"
    mock_llm_client.get_response.assert_called_once()

    # Проверяем, что сообщение сохранено
    context = manager.storage.get_context(123)
    assert context is not None
    assert len(context.messages) == 1
    assert len(context.responses) == 1


@pytest.mark.asyncio
async def test_process_multiple_messages(mock_llm_client):
    """Тест: Обработка нескольких сообщений"""
    manager = ConversationManager(mock_llm_client, "System prompt")

    await manager.process_message(123, "First")
    await manager.process_message(123, "Second")

    context = manager.storage.get_context(123)
    assert context is not None
    assert len(context.messages) == 2
    assert len(context.responses) == 2


def test_clear_history(mock_llm_client):
    """Тест: Очистка истории"""
    manager = ConversationManager(mock_llm_client, "System prompt")
    manager.storage.add_message(123, "Hello", "System prompt")

    assert manager.storage.get_context(123) is not None

    manager.clear_history(123)
    assert manager.storage.get_context(123) is None

