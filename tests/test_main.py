"""Тесты для главной функции приложения"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.main import main


@pytest.mark.asyncio
async def test_main_success() -> None:
    """Тест успешного запуска приложения"""
    # Мокирование всех зависимостей
    with (
        patch("src.main.Config") as mock_config_class,
        patch("src.main.LLMClient") as mock_llm_class,
        patch("src.main.ConversationManager") as mock_conv_class,
        patch("src.main.TelegramBot") as mock_bot_class,
    ):
        # Настройка mock Config
        mock_config = Mock()
        mock_config.openrouter_key = "test-key"
        mock_config.default_model = "test-model"
        mock_config.max_tokens = 100
        mock_config.temperature = 0.7
        mock_config.telegram_token = "test-token"
        mock_config.system_prompt = "Test prompt"
        mock_config.max_history_messages = 10
        mock_config_class.return_value = mock_config

        # Настройка mock TelegramBot
        mock_bot = Mock()
        mock_bot.start_polling = AsyncMock(side_effect=KeyboardInterrupt())
        mock_bot.stop = AsyncMock()
        mock_bot_class.return_value = mock_bot

        # Запуск main
        await main()

        # Проверки
        mock_config_class.assert_called_once()
        mock_llm_class.assert_called_once_with(
            api_key="test-key",
            model="test-model",
            max_tokens=100,
            temperature=0.7,
        )
        mock_conv_class.assert_called_once()
        mock_bot_class.assert_called_once()
        mock_bot.start_polling.assert_called_once()
        mock_bot.stop.assert_called_once()


@pytest.mark.asyncio
async def test_main_config_error() -> None:
    """Тест обработки ошибки конфигурации"""
    with (
        patch("src.main.Config") as mock_config_class,
        pytest.raises(SystemExit) as exc_info,
    ):
        # Config выбрасывает ValueError
        mock_config_class.side_effect = ValueError("Missing TELEGRAM_TOKEN")

        # Запуск main
        await main()

    # Проверка exit code
    assert exc_info.value.code == 1


@pytest.mark.asyncio
async def test_main_keyboard_interrupt() -> None:
    """Тест обработки Ctrl+C (KeyboardInterrupt)"""
    with (
        patch("src.main.Config") as mock_config_class,
        patch("src.main.LLMClient"),
        patch("src.main.ConversationManager"),
        patch("src.main.TelegramBot") as mock_bot_class,
    ):
        # Настройка mock Config
        mock_config = Mock()
        mock_config.openrouter_key = "test-key"
        mock_config.default_model = "test-model"
        mock_config.max_tokens = 100
        mock_config.temperature = 0.7
        mock_config.telegram_token = "test-token"
        mock_config.system_prompt = "Test prompt"
        mock_config.max_history_messages = 10
        mock_config_class.return_value = mock_config

        # Настройка mock TelegramBot с KeyboardInterrupt
        mock_bot = Mock()
        mock_bot.start_polling = AsyncMock(side_effect=KeyboardInterrupt())
        mock_bot.stop = AsyncMock()
        mock_bot_class.return_value = mock_bot

        # Запуск main (не должен вызвать SystemExit)
        await main()

        # Проверка, что stop был вызван
        mock_bot.stop.assert_called_once()


@pytest.mark.asyncio
async def test_main_unexpected_error() -> None:
    """Тест обработки неожиданной ошибки"""
    with (
        patch("src.main.Config") as mock_config_class,
        patch("src.main.LLMClient"),
        patch("src.main.ConversationManager"),
        patch("src.main.TelegramBot") as mock_bot_class,
        pytest.raises(SystemExit) as exc_info,
    ):
        # Настройка mock Config
        mock_config = Mock()
        mock_config.openrouter_key = "test-key"
        mock_config.default_model = "test-model"
        mock_config.max_tokens = 100
        mock_config.temperature = 0.7
        mock_config.telegram_token = "test-token"
        mock_config.system_prompt = "Test prompt"
        mock_config.max_history_messages = 10
        mock_config_class.return_value = mock_config

        # Настройка mock TelegramBot с неожиданной ошибкой
        mock_bot = Mock()
        mock_bot.start_polling = AsyncMock(side_effect=RuntimeError("Unexpected error"))
        mock_bot.stop = AsyncMock()
        mock_bot_class.return_value = mock_bot

        # Запуск main
        await main()

    # Проверка exit code
    assert exc_info.value.code == 1


@pytest.mark.asyncio
async def test_main_bot_not_initialized_on_config_error() -> None:
    """Тест, что бот не останавливается, если не был инициализирован"""
    with (
        patch("src.main.Config") as mock_config_class,
        pytest.raises(SystemExit),
    ):
        # Config выбрасывает ValueError (бот не инициализируется)
        mock_config_class.side_effect = ValueError("Config error")

        # Запуск main (не должен вызвать ошибку в finally блоке)
        await main()


@pytest.mark.asyncio
async def test_main_bot_stops_on_error() -> None:
    """Тест, что бот корректно останавливается при ошибке"""
    with (
        patch("src.main.Config") as mock_config_class,
        patch("src.main.LLMClient"),
        patch("src.main.ConversationManager"),
        patch("src.main.TelegramBot") as mock_bot_class,
        pytest.raises(SystemExit),
    ):
        # Настройка mock Config
        mock_config = Mock()
        mock_config.openrouter_key = "test-key"
        mock_config.default_model = "test-model"
        mock_config.max_tokens = 100
        mock_config.temperature = 0.7
        mock_config.telegram_token = "test-token"
        mock_config.system_prompt = "Test prompt"
        mock_config.max_history_messages = 10
        mock_config_class.return_value = mock_config

        # Настройка mock TelegramBot
        mock_bot = Mock()
        mock_bot.start_polling = AsyncMock(side_effect=Exception("Test error"))
        mock_bot.stop = AsyncMock()
        mock_bot_class.return_value = mock_bot

        # Запуск main
        await main()

        # Проверка, что stop был вызван
        mock_bot.stop.assert_called_once()

