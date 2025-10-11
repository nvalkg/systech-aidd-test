"""Тесты для модуля config"""

from pathlib import Path

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


class TestConfigSystemPrompt:
    """Тесты для загрузки системного промпта"""

    def test_config_system_prompt_from_env(self, valid_env, monkeypatch) -> None:
        """Тест: промпт загружается из переменной SYSTEM_PROMPT"""
        # Arrange
        custom_prompt = "You are a custom assistant from env."
        monkeypatch.setenv("SYSTEM_PROMPT", custom_prompt)

        # Act
        config = Config()

        # Assert
        assert config.system_prompt == custom_prompt

    def test_config_system_prompt_from_file(self, valid_env, monkeypatch, tmp_path: Path) -> None:
        """Тест: промпт загружается из файла через SYSTEM_PROMPT_FILE"""
        # Arrange: создаём временный файл с промптом
        prompt_file = tmp_path / "test_prompt.txt"
        file_prompt = "Роль: File Assistant\n\nYou are loaded from file."
        prompt_file.write_text(file_prompt, encoding="utf-8")

        monkeypatch.setenv("SYSTEM_PROMPT_FILE", str(prompt_file))

        # Act
        config = Config()

        # Assert
        assert config.system_prompt == file_prompt
        assert config.system_prompt_file == str(prompt_file)

    def test_config_system_prompt_file_priority(
        self, valid_env, monkeypatch, tmp_path: Path
    ) -> None:
        """Тест: SYSTEM_PROMPT_FILE имеет приоритет над SYSTEM_PROMPT"""
        # Arrange
        prompt_file = tmp_path / "priority_test.txt"
        file_prompt = "File prompt with priority"
        prompt_file.write_text(file_prompt, encoding="utf-8")

        env_prompt = "Env prompt should be ignored"

        monkeypatch.setenv("SYSTEM_PROMPT_FILE", str(prompt_file))
        monkeypatch.setenv("SYSTEM_PROMPT", env_prompt)

        # Act
        config = Config()

        # Assert: должен использовать файл, а не env
        assert config.system_prompt == file_prompt
        assert config.system_prompt != env_prompt

    def test_config_system_prompt_file_not_found(self, valid_env, monkeypatch) -> None:
        """Тест: fallback на SYSTEM_PROMPT при отсутствии файла"""
        # Arrange
        non_existent_file = "non_existent_prompt.txt"
        fallback_prompt = "Fallback prompt from env"

        monkeypatch.setenv("SYSTEM_PROMPT_FILE", non_existent_file)
        monkeypatch.setenv("SYSTEM_PROMPT", fallback_prompt)

        # Act
        config = Config()

        # Assert: должен использовать fallback из SYSTEM_PROMPT
        assert config.system_prompt == fallback_prompt
