"""Тесты для модуля config"""

import pytest

from src.config import Config


def test_config_valid(valid_env):
    """Тест: Config успешно загружается с валидными env переменными"""
    config = Config()

    assert config.telegram_token == "test_telegram_token"
    assert config.openrouter_key == "test_openrouter_key"
    assert config.default_model == "openai/gpt-3.5-turbo"
    assert config.max_tokens == 1000
    assert config.temperature == 0.7
    assert config.max_history_messages == 10


def test_config_missing_telegram_token(clean_env, monkeypatch):
    """Тест: ValueError при отсутствии TELEGRAM_BOT_TOKEN"""
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_key")

    with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN"):
        Config()


def test_config_missing_openrouter_key(clean_env, monkeypatch):
    """Тест: ValueError при отсутствии OPENROUTER_API_KEY"""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")

    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        Config()


def test_config_invalid_max_tokens(valid_env, monkeypatch):
    """Тест: ValueError при невалидном MAX_TOKENS"""
    monkeypatch.setenv("MAX_TOKENS", "not_a_number")

    with pytest.raises(ValueError, match="MAX_TOKENS должно быть целым числом"):
        Config()


def test_config_invalid_temperature(valid_env, monkeypatch):
    """Тест: ValueError при невалидном TEMPERATURE"""
    monkeypatch.setenv("TEMPERATURE", "invalid")

    with pytest.raises(ValueError, match="TEMPERATURE должно быть числом"):
        Config()


def test_config_custom_values(valid_env, monkeypatch):
    """Тест: Config правильно использует кастомные значения"""
    monkeypatch.setenv("DEFAULT_MODEL", "custom/model")
    monkeypatch.setenv("MAX_TOKENS", "500")
    monkeypatch.setenv("TEMPERATURE", "0.5")
    monkeypatch.setenv("MAX_HISTORY_MESSAGES", "20")

    config = Config()

    assert config.default_model == "custom/model"
    assert config.max_tokens == 500
    assert config.temperature == 0.5
    assert config.max_history_messages == 20


def test_config_defaults(valid_env):
    """Тест: Config использует дефолтные значения"""
    config = Config()

    # Проверяем значения по умолчанию
    assert config.default_model == "openai/gpt-3.5-turbo"
    assert config.max_tokens == 1000
    assert config.temperature == 0.7
    assert config.max_history_messages == 10
    assert config.system_prompt == "You are a helpful AI assistant."
    assert config.log_level == "INFO"

