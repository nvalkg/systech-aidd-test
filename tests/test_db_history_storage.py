"""Тесты для модуля db_history_storage"""

import pytest

from src.db_history_storage import DatabaseHistoryStorage


@pytest.mark.asyncio
async def test_db_history_storage_init(test_db_engine):
    """Тест: DatabaseHistoryStorage инициализируется корректно"""
    storage = DatabaseHistoryStorage(test_db_engine, max_history=5)
    assert storage.max_history == 5
    assert storage.engine == test_db_engine


@pytest.mark.asyncio
async def test_add_message(test_db_engine):
    """Тест: Добавление сообщения пользователя"""
    storage = DatabaseHistoryStorage(test_db_engine)
    await storage.add_message(123, "Hello", "System prompt")

    context = await storage.get_context(123)
    assert context is not None
    assert len(context.messages) == 1
    assert context.messages[0].text == "Hello"
    assert context.messages[0].user_id == 123
    assert context.messages[0].content_length == 5


@pytest.mark.asyncio
async def test_add_response(test_db_engine):
    """Тест: Добавление ответа LLM"""
    storage = DatabaseHistoryStorage(test_db_engine)
    await storage.add_message(123, "Hello", "System prompt")
    await storage.add_response(123, "Hi there", "gpt-3.5")

    context = await storage.get_context(123)
    assert context is not None
    assert len(context.responses) == 1
    assert context.responses[0].content == "Hi there"
    assert context.responses[0].model_used == "gpt-3.5"
    assert context.responses[0].content_length == 8


@pytest.mark.asyncio
async def test_trim_history(test_db_engine):
    """Тест: Обрезка истории до max_history"""
    storage = DatabaseHistoryStorage(test_db_engine, max_history=3)

    # Добавляем 5 сообщений
    for i in range(5):
        await storage.add_message(123, f"Message {i}", "System prompt")
        await storage.add_response(123, f"Response {i}", "gpt-3.5")

    context = await storage.get_context(123)
    assert context is not None
    assert len(context.messages) == 3
    assert len(context.responses) == 3
    # Проверяем, что остались последние 3
    assert context.messages[0].text == "Message 2"
    assert context.messages[2].text == "Message 4"


@pytest.mark.asyncio
async def test_clear_history(test_db_engine):
    """Тест: Очистка истории (soft delete)"""
    storage = DatabaseHistoryStorage(test_db_engine)
    await storage.add_message(123, "Hello", "System prompt")
    await storage.add_response(123, "Hi", "gpt-3.5")

    assert await storage.get_context(123) is not None

    await storage.clear(123)

    context = await storage.get_context(123)
    # После soft delete контекст существует, но сообщения удалены
    assert context is not None
    assert len(context.messages) == 0
    assert len(context.responses) == 0


@pytest.mark.asyncio
async def test_get_nonexistent_context(test_db_engine):
    """Тест: Получение несуществующего контекста"""
    storage = DatabaseHistoryStorage(test_db_engine)
    context = await storage.get_context(999)
    assert context is None


@pytest.mark.asyncio
async def test_get_or_create_context(test_db_engine):
    """Тест: Получение или создание контекста"""
    storage = DatabaseHistoryStorage(test_db_engine)

    # Первый вызов создает контекст
    context1 = await storage.get_or_create_context(123, "System prompt")
    assert context1 is not None
    assert context1.user_id == 123
    assert context1.system_prompt == "System prompt"
    assert len(context1.messages) == 0

    # Добавляем сообщение
    await storage.add_message(123, "Test", "System prompt")

    # Второй вызов возвращает существующий контекст
    context2 = await storage.get_or_create_context(123, "System prompt")
    assert context2 is not None
    assert len(context2.messages) == 1
    assert context2.messages[0].text == "Test"


@pytest.mark.asyncio
async def test_multiple_users(test_db_engine):
    """Тест: Изоляция данных разных пользователей"""
    storage = DatabaseHistoryStorage(test_db_engine)

    # Добавляем сообщения от двух пользователей
    await storage.add_message(123, "User 123 message", "System prompt")
    await storage.add_message(456, "User 456 message", "System prompt")

    # Проверяем изоляцию
    context_123 = await storage.get_context(123)
    context_456 = await storage.get_context(456)

    assert context_123 is not None
    assert context_456 is not None
    assert len(context_123.messages) == 1
    assert len(context_456.messages) == 1
    assert context_123.messages[0].text == "User 123 message"
    assert context_456.messages[0].text == "User 456 message"
