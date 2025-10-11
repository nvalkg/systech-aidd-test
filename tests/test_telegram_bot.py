"""Тесты для модуля telegram_bot"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram.types import Message, User

from src.telegram_bot import (
    CLEAR_TEXT,
    ERROR_MESSAGE_GENERAL,
    HELP_TEXT,
    MAX_MESSAGE_LENGTH,
    WELCOME_TEXT,
    TelegramBot,
)


@pytest.fixture
def mock_conversation_manager():
    """Мок ConversationManager"""
    manager = AsyncMock()
    manager.process_message = AsyncMock(return_value="Test response from LLM")
    manager.clear_history = MagicMock()
    return manager


@pytest.fixture
def mock_message():
    """Мок Message от Telegram"""
    message = MagicMock(spec=Message)
    message.from_user = MagicMock(spec=User)
    message.from_user.id = 12345
    message.from_user.username = "testuser"
    message.from_user.first_name = "Test"
    message.answer = AsyncMock()
    message.text = "Hello bot"
    return message


@pytest.fixture
def telegram_bot(mock_conversation_manager):
    """Фикстура TelegramBot с моком ConversationManager"""
    # Мокируем Bot и Dispatcher, чтобы не создавать реальные
    with pytest.MonkeyPatch.context() as mp:
        mock_bot = MagicMock()
        mock_dp = MagicMock()
        mock_dp.message = MagicMock()
        mock_dp.message.register = MagicMock()

        mp.setattr("src.telegram_bot.Bot", lambda token: mock_bot)
        mp.setattr("src.telegram_bot.Dispatcher", lambda: mock_dp)

        bot = TelegramBot("fake_token", mock_conversation_manager)
        return bot


def test_get_user_info(telegram_bot, mock_message):
    """Тест: метод _get_user_info извлекает данные пользователя"""
    user_id, username = telegram_bot._get_user_info(mock_message)

    assert user_id == 12345
    assert username == "testuser"


def test_get_user_info_no_username(telegram_bot, mock_message):
    """Тест: _get_user_info использует first_name если нет username"""
    mock_message.from_user.username = None

    user_id, username = telegram_bot._get_user_info(mock_message)

    assert user_id == 12345
    assert username == "Test"


def test_get_user_info_no_user(telegram_bot, mock_message):
    """Тест: _get_user_info выбрасывает ValueError если нет from_user"""
    mock_message.from_user = None

    with pytest.raises(ValueError, match="Message has no user information"):
        telegram_bot._get_user_info(mock_message)


@pytest.mark.asyncio
async def test_cmd_start(telegram_bot, mock_message):
    """Тест: команда /start отправляет приветствие"""
    await telegram_bot.cmd_start(mock_message)

    mock_message.answer.assert_called_once_with(WELCOME_TEXT)


@pytest.mark.asyncio
async def test_cmd_help(telegram_bot, mock_message):
    """Тест: команда /help отправляет справку"""
    await telegram_bot.cmd_help(mock_message)

    mock_message.answer.assert_called_once_with(HELP_TEXT)


@pytest.mark.asyncio
async def test_cmd_clear(telegram_bot, mock_message):
    """Тест: команда /clear очищает историю"""
    await telegram_bot.cmd_clear(mock_message)

    # Проверяем, что история очищена
    telegram_bot.conversation_manager.clear_history.assert_called_once_with(12345)
    # Проверяем, что отправлено подтверждение
    mock_message.answer.assert_called_once_with(CLEAR_TEXT)


@pytest.mark.asyncio
async def test_handle_empty_message(telegram_bot, mock_message):
    """Тест: пустые сообщения игнорируются"""
    mock_message.text = "   "

    await telegram_bot.handle_message(mock_message)

    # Сообщение не должно быть обработано
    telegram_bot.conversation_manager.process_message.assert_not_called()
    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_handle_none_message(telegram_bot, mock_message):
    """Тест: None сообщения игнорируются"""
    mock_message.text = None

    await telegram_bot.handle_message(mock_message)

    telegram_bot.conversation_manager.process_message.assert_not_called()
    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_handle_long_message(telegram_bot, mock_message):
    """Тест: длинные сообщения отклоняются"""
    mock_message.text = "a" * (MAX_MESSAGE_LENGTH + 1)

    await telegram_bot.handle_message(mock_message)

    # Проверяем, что сообщение не обработано
    telegram_bot.conversation_manager.process_message.assert_not_called()
    # Проверяем, что отправлена ошибка
    mock_message.answer.assert_called_once()
    error_text = mock_message.answer.call_args[0][0]
    assert "слишком длинное" in error_text.lower()


@pytest.mark.asyncio
async def test_handle_message_success(telegram_bot, mock_message):
    """Тест: успешная обработка сообщения"""
    mock_message.text = "Hello bot"

    await telegram_bot.handle_message(mock_message)

    # Проверяем, что сообщение обработано
    telegram_bot.conversation_manager.process_message.assert_called_once_with(12345, "Hello bot")
    # Проверяем, что отправлен ответ
    mock_message.answer.assert_called_once_with("Test response from LLM")


@pytest.mark.asyncio
async def test_handle_message_error(telegram_bot, mock_message):
    """Тест: обработка ошибки при работе с ConversationManager"""
    telegram_bot.conversation_manager.process_message.side_effect = Exception("Test error")
    mock_message.text = "Hello bot"

    await telegram_bot.handle_message(mock_message)

    # Проверяем, что отправлена ошибка
    mock_message.answer.assert_called_once_with(ERROR_MESSAGE_GENERAL)


class TestCmdRole:
    """Тесты для команды /role"""

    @pytest.mark.asyncio
    async def test_cmd_role_default_prompt(self, telegram_bot, mock_message) -> None:
        """Тест: команда /role с дефолтным промптом"""
        # Arrange: мокируем get_role_description для дефолтного промпта
        telegram_bot.conversation_manager.get_role_description = MagicMock(
            return_value="🤖 Моя роль: AI Assistant\n\nYou are a helpful AI assistant."
        )

        # Act
        await telegram_bot.cmd_role(mock_message)

        # Assert
        mock_message.answer.assert_called_once()
        response_text = mock_message.answer.call_args[0][0]
        assert "🤖 Моя роль: AI Assistant" in response_text
        assert "helpful AI assistant" in response_text

    @pytest.mark.asyncio
    async def test_cmd_role_specialized_prompt(self, telegram_bot, mock_message) -> None:
        """Тест: команда /role со специализированным промптом"""
        # Arrange: мокируем get_role_description для специализированного промпта
        specialized_description = """🤖 Моя роль: Python Code Reviewer Expert

Ты - опытный Python разработчик с 10+ годами опыта."""

        telegram_bot.conversation_manager.get_role_description = MagicMock(
            return_value=specialized_description
        )

        # Act
        await telegram_bot.cmd_role(mock_message)

        # Assert
        mock_message.answer.assert_called_once()
        response_text = mock_message.answer.call_args[0][0]
        assert "Python Code Reviewer Expert" in response_text
        assert "опытный Python разработчик" in response_text

    @pytest.mark.asyncio
    async def test_cmd_role_formatting(self, telegram_bot, mock_message) -> None:
        """Тест: проверка форматирования ответа команды /role"""
        # Arrange
        role_description = "🤖 Моя роль: Test Role\n\nTest description."
        telegram_bot.conversation_manager.get_role_description = MagicMock(
            return_value=role_description
        )

        # Act
        await telegram_bot.cmd_role(mock_message)

        # Assert
        mock_message.answer.assert_called_once_with(role_description)

    @pytest.mark.asyncio
    async def test_cmd_role_user_info_logging(self, telegram_bot, mock_message) -> None:
        """Тест: команда /role логирует информацию о пользователе"""
        # Arrange
        telegram_bot.conversation_manager.get_role_description = MagicMock(
            return_value="Test role description"
        )

        # Act
        await telegram_bot.cmd_role(mock_message)

        # Assert: проверяем, что не было ошибок при извлечении user_info
        # (метод _get_user_info должен вызваться внутри cmd_role)
        mock_message.answer.assert_called_once()
