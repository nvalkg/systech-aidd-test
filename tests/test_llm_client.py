"""Тесты для LLMClient"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.llm_client import LLMClient


@pytest.fixture
def llm_client() -> LLMClient:
    """Фикстура с LLMClient"""
    return LLMClient(
        api_key="test-api-key",
        model="test-model",
        max_tokens=100,
        temperature=0.7,
    )


@pytest.mark.asyncio
async def test_llm_client_init(llm_client: LLMClient) -> None:
    """Тест инициализации LLMClient"""
    assert llm_client.model == "test-model"
    assert llm_client.max_tokens == 100
    assert llm_client.temperature == 0.7
    assert llm_client.client is not None


@pytest.mark.asyncio
async def test_get_response_success(llm_client: LLMClient) -> None:
    """Тест успешного получения ответа от LLM"""
    # Подготовка mock ответа
    mock_message = Mock()
    mock_message.content = "Test response from LLM"

    mock_choice = Mock()
    mock_choice.message = mock_message

    mock_usage = Mock()
    mock_usage.total_tokens = 50

    mock_response = Mock()
    mock_response.choices = [mock_choice]
    mock_response.usage = mock_usage

    # Мокирование вызова API
    with patch.object(
        llm_client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = mock_response

        # Вызов метода
        messages = [{"role": "user", "content": "Hello"}]
        result = await llm_client.get_response(messages)

        # Проверки
        assert result == "Test response from LLM"
        mock_create.assert_called_once_with(
            model="test-model",
            messages=messages,
            max_tokens=100,
            temperature=0.7,
        )


@pytest.mark.asyncio
async def test_get_response_no_usage(llm_client: LLMClient) -> None:
    """Тест обработки ответа без usage информации"""
    # Подготовка mock ответа без usage
    mock_message = Mock()
    mock_message.content = "Response without usage"

    mock_choice = Mock()
    mock_choice.message = mock_message

    mock_response = Mock()
    mock_response.choices = [mock_choice]
    mock_response.usage = None  # Отсутствует usage

    # Мокирование вызова API
    with patch.object(
        llm_client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = mock_response

        # Вызов метода
        messages = [{"role": "user", "content": "Hello"}]
        result = await llm_client.get_response(messages)

        # Проверки
        assert result == "Response without usage"
        # Проверяем, что отсутствие usage не вызывает ошибку


@pytest.mark.asyncio
async def test_get_response_api_error(llm_client: LLMClient) -> None:
    """Тест обработки ошибки API"""
    # Мокирование ошибки API
    with patch.object(
        llm_client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.side_effect = Exception("API Error: Rate limit exceeded")

        # Вызов метода должен пробросить исключение
        messages = [{"role": "user", "content": "Hello"}]
        with pytest.raises(Exception, match="API Error: Rate limit exceeded"):
            await llm_client.get_response(messages)


@pytest.mark.asyncio
async def test_get_response_empty_content(llm_client: LLMClient) -> None:
    """Тест обработки пустого ответа от LLM"""
    # Подготовка mock ответа с пустым content
    mock_message = Mock()
    mock_message.content = ""

    mock_choice = Mock()
    mock_choice.message = mock_message

    mock_usage = Mock()
    mock_usage.total_tokens = 10

    mock_response = Mock()
    mock_response.choices = [mock_choice]
    mock_response.usage = mock_usage

    # Мокирование вызова API
    with patch.object(
        llm_client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = mock_response

        # Вызов метода
        messages = [{"role": "user", "content": "Hello"}]
        result = await llm_client.get_response(messages)

        # Проверки
        assert result == ""


@pytest.mark.asyncio
async def test_get_response_multiple_messages(llm_client: LLMClient) -> None:
    """Тест работы с несколькими сообщениями в истории"""
    # Подготовка mock ответа
    mock_message = Mock()
    mock_message.content = "Response to conversation"

    mock_choice = Mock()
    mock_choice.message = mock_message

    mock_usage = Mock()
    mock_usage.total_tokens = 150

    mock_response = Mock()
    mock_response.choices = [mock_choice]
    mock_response.usage = mock_usage

    # Мокирование вызова API
    with patch.object(
        llm_client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = mock_response

        # Вызов метода с несколькими сообщениями
        messages = [
            {"role": "system", "content": "You are helpful assistant"},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi!"},
            {"role": "user", "content": "How are you?"},
        ]
        result = await llm_client.get_response(messages)

        # Проверки
        assert result == "Response to conversation"
        mock_create.assert_called_once_with(
            model="test-model",
            messages=messages,
            max_tokens=100,
            temperature=0.7,
        )

