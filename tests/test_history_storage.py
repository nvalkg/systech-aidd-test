"""Тесты для модуля history_storage"""

import pytest

from src.history_storage import HistoryStorage


def test_history_storage_init():
    """Тест: HistoryStorage инициализируется корректно"""
    storage = HistoryStorage(max_history=5)
    assert storage.max_history == 5
    assert storage.contexts == {}


def test_add_message():
    """Тест: Добавление сообщения пользователя"""
    storage = HistoryStorage()
    storage.add_message(123, "Hello", "System prompt")

    context = storage.get_context(123)
    assert context is not None
    assert len(context.messages) == 1
    assert context.messages[0].text == "Hello"
    assert context.messages[0].user_id == 123


def test_add_response():
    """Тест: Добавление ответа LLM"""
    storage = HistoryStorage()
    storage.add_message(123, "Hello", "System prompt")
    storage.add_response(123, "Hi there", "gpt-3.5")

    context = storage.get_context(123)
    assert context is not None
    assert len(context.responses) == 1
    assert context.responses[0].content == "Hi there"
    assert context.responses[0].model_used == "gpt-3.5"


def test_trim_history():
    """Тест: Обрезка истории до max_history"""
    storage = HistoryStorage(max_history=3)

    # Добавляем 5 сообщений
    for i in range(5):
        storage.add_message(123, f"Message {i}", "System prompt")
        storage.add_response(123, f"Response {i}", "gpt-3.5")

    context = storage.get_context(123)
    assert context is not None
    assert len(context.messages) == 3
    assert len(context.responses) == 3
    # Проверяем, что остались последние 3
    assert context.messages[0].text == "Message 2"
    assert context.messages[2].text == "Message 4"


def test_clear_history():
    """Тест: Очистка истории"""
    storage = HistoryStorage()
    storage.add_message(123, "Hello", "System prompt")

    assert storage.get_context(123) is not None

    storage.clear(123)
    assert storage.get_context(123) is None


def test_get_nonexistent_context():
    """Тест: Получение несуществующего контекста"""
    storage = HistoryStorage()
    context = storage.get_context(999)
    assert context is None

