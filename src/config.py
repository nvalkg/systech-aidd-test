"""Конфигурация приложения из переменных окружения"""

import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


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
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")

        # Системный промпт: загрузка из файла или текста
        self.system_prompt_file: str | None = os.getenv("SYSTEM_PROMPT_FILE")
        self.system_prompt_text: str = os.getenv("SYSTEM_PROMPT", "You are a helpful AI assistant.")
        self.system_prompt: str = self._load_system_prompt()

        # База данных
        self.database_url: str = os.getenv(
            "DATABASE_URL", "postgresql+asyncpg://aidd:aidd_dev_password@localhost:5433/aidd"
        )

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

    def _load_system_prompt(self) -> str:
        """
        Загрузка системного промпта с приоритетом: FILE → TEXT → default

        Returns:
            str: Загруженный системный промпт
        """
        if self.system_prompt_file:
            try:
                with open(self.system_prompt_file, encoding="utf-8") as f:
                    content = f.read().strip()
                    logger.info(f"Системный промпт загружен из файла: {self.system_prompt_file}")
                    return content
            except FileNotFoundError:
                logger.warning(
                    f"Файл {self.system_prompt_file} не найден, используется SYSTEM_PROMPT"
                )

        return self.system_prompt_text
