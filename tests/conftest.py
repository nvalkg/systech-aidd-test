"""Фикстуры для pytest"""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.database import metadata


@pytest.fixture
def clean_env(monkeypatch):
    """Очистить переменные окружения для тестов"""
    # Мокируем load_dotenv, чтобы она ничего не загружала из .env
    monkeypatch.setattr("src.config.load_dotenv", lambda: None)

    # Удаляем все переменные окружения, которые может использовать Config
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("DEFAULT_MODEL", raising=False)
    monkeypatch.delenv("MAX_TOKENS", raising=False)
    monkeypatch.delenv("TEMPERATURE", raising=False)
    monkeypatch.delenv("MAX_HISTORY_MESSAGES", raising=False)
    monkeypatch.delenv("SYSTEM_PROMPT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)


@pytest.fixture
def valid_env(monkeypatch):
    """Установить валидные переменные окружения"""
    # Мокируем load_dotenv, чтобы она ничего не загружала из .env
    monkeypatch.setattr("src.config.load_dotenv", lambda: None)

    # Удаляем все переменные из .env (если они были загружены ранее)
    monkeypatch.delenv("DEFAULT_MODEL", raising=False)
    monkeypatch.delenv("MAX_TOKENS", raising=False)
    monkeypatch.delenv("TEMPERATURE", raising=False)
    monkeypatch.delenv("MAX_HISTORY_MESSAGES", raising=False)
    monkeypatch.delenv("SYSTEM_PROMPT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    # Устанавливаем валидные тестовые значения
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_telegram_token")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_openrouter_key")


@pytest_asyncio.fixture
async def test_db_engine() -> AsyncEngine:
    """Создать тестовый движок БД с SQLite in-memory"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )

    # Создаем все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield engine

    # Очищаем после теста
    await engine.dispose()
