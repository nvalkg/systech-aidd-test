"""Конфигурация приложения из переменных окружения"""

import os

from dotenv import load_dotenv


class Config:
    """Класс для загрузки и валидации конфигурации из .env файла"""

    def __init__(self) -> None:
        """Инициализация конфигурации с загрузкой переменных окружения"""
        load_dotenv()

        # Обязательные параметры
        self.telegram_token: str = self._get_required_env("TELEGRAM_BOT_TOKEN")
        self.openrouter_key: str = self._get_required_env("OPENROUTER_API_KEY")

        # Необязательные параметры с значениями по умолчанию
        self.default_model: str = os.getenv("DEFAULT_MODEL", "openai/gpt-3.5-turbo")
        self.max_tokens: int = self._parse_int("MAX_TOKENS", 1000)
        self.temperature: float = self._parse_float("TEMPERATURE", 0.7)
        self.max_history_messages: int = self._parse_int("MAX_HISTORY_MESSAGES", 10)
        self.system_prompt: str = os.getenv("SYSTEM_PROMPT", "You are a helpful AI assistant.")
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def _get_required_env(self, key: str) -> str:
        """Получить обязательную переменную окружения"""
        value = os.getenv(key, "")
        if not value:
            raise ValueError(f"{key} не установлен в .env файле")
        return value

    def _parse_int(self, key: str, default: int) -> int:
        """Безопасно распарсить int из переменной окружения"""
        value = os.getenv(key, str(default))
        try:
            return int(value)
        except ValueError as e:
            raise ValueError(f"{key} должно быть целым числом, получено: {value!r}") from e

    def _parse_float(self, key: str, default: float) -> float:
        """Безопасно распарсить float из переменной окружения"""
        value = os.getenv(key, str(default))
        try:
            return float(value)
        except ValueError as e:
            raise ValueError(f"{key} должно быть числом, получено: {value!r}") from e
