"""Тесты для модуля conversation_manager"""

from unittest.mock import AsyncMock

import pytest

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


class TestGetRoleDescription:
    """Тесты для метода get_role_description"""

    def test_get_role_description(self, mock_llm_client) -> None:
        """Тест: получение описания роли"""
        # Arrange
        system_prompt = "Роль: Test Assistant\n\nYou are a test assistant."
        manager = ConversationManager(mock_llm_client, system_prompt)

        # Act
        description = manager.get_role_description()

        # Assert
        assert isinstance(description, str)
        assert len(description) > 0
        # Должно содержать информацию о роли
        assert "роль" in description.lower() or "role" in description.lower()

    def test_get_role_description_integration(self, mock_llm_client) -> None:
        """Тест: интеграция с PromptLoader для получения описания роли"""
        # Arrange
        specialized_prompt = """Роль: Python Code Reviewer Expert

Ты - опытный Python разработчик с 10+ годами опыта, специализирующийся на code review.

Твои принципы:
- SOLID, DRY, KISS - основа твоих рекомендаций"""

        manager = ConversationManager(mock_llm_client, specialized_prompt)

        # Act
        description = manager.get_role_description()

        # Assert
        assert "Python Code Reviewer Expert" in description
        assert "🤖" in description  # Emoji должно быть в форматировании
