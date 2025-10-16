"""Схема базы данных и подключение"""

import logging
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

logger = logging.getLogger(__name__)

# Метаданные для SQLAlchemy Core
metadata = MetaData()

# Таблица conversations - контексты диалогов
conversations = Table(
    "conversations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, nullable=False),
    Column("system_prompt", Text, nullable=False),
    Column("created_at", DateTime, nullable=False, default=datetime.now),
    Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now),
    # Индекс для быстрого поиска по user_id
    Index("idx_conversations_user_id", "user_id"),
)

# Таблица user_messages - сообщения пользователей
user_messages = Table(
    "user_messages",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "conversation_id",
        Integer,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("user_id", BigInteger, nullable=False),
    Column("text", Text, nullable=False),
    Column("content_length", Integer, nullable=False),
    Column("timestamp", DateTime, nullable=False, default=datetime.now),
    Column("is_deleted", Boolean, nullable=False, default=False),
    # Индексы для оптимизации запросов
    Index("idx_user_messages_conversation_id", "conversation_id"),
    Index("idx_user_messages_user_id", "user_id"),
    Index("idx_user_messages_is_deleted", "is_deleted"),
)

# Таблица llm_responses - ответы LLM
llm_responses = Table(
    "llm_responses",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "conversation_id",
        Integer,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("content", Text, nullable=False),
    Column("content_length", Integer, nullable=False),
    Column("model_used", String(100), nullable=False),
    Column("timestamp", DateTime, nullable=False, default=datetime.now),
    Column("is_deleted", Boolean, nullable=False, default=False),
    # Индексы для оптимизации запросов
    Index("idx_llm_responses_conversation_id", "conversation_id"),
    Index("idx_llm_responses_is_deleted", "is_deleted"),
)


def create_engine(database_url: str) -> AsyncEngine:
    """
    Создать асинхронный движок SQLAlchemy

    Args:
        database_url: URL подключения к базе данных

    Returns:
        Асинхронный движок SQLAlchemy
    """
    engine = create_async_engine(
        database_url,
        echo=False,  # Отключаем вывод SQL запросов в лог
        pool_pre_ping=True,  # Проверка соединения перед использованием
        pool_size=5,  # Размер пула соединений
        max_overflow=10,  # Максимальное количество дополнительных соединений
    )
    logger.info(f"Создан движок БД: {database_url.split('@')[0]}@***")
    return engine
