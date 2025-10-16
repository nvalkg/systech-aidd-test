"""Хранение истории диалогов в базе данных (Repository pattern)"""

import logging
from datetime import datetime

from sqlalchemy import and_, insert, select, update
from sqlalchemy.ext.asyncio import AsyncEngine

from .database import conversations, llm_responses, user_messages
from .models import ConversationContext, LLMResponse, UserMessage

logger = logging.getLogger(__name__)


class DatabaseHistoryStorage:
    """Хранилище истории диалогов в PostgreSQL с использованием Repository pattern"""

    def __init__(self, engine: AsyncEngine, max_history: int = 10) -> None:
        """
        Инициализация хранилища

        Args:
            engine: Асинхронный движок SQLAlchemy
            max_history: Максимальное количество сообщений в истории
        """
        self.engine = engine
        self.max_history = max_history
        logger.info(f"DatabaseHistoryStorage инициализирован (max_history={max_history})")

    async def get_or_create_context(self, user_id: int, system_prompt: str) -> ConversationContext:
        """
        Получить или создать контекст для пользователя

        Args:
            user_id: ID пользователя
            system_prompt: Системный промпт

        Returns:
            Контекст диалога пользователя
        """
        async with self.engine.begin() as conn:
            # Проверяем, есть ли активный диалог для пользователя
            result = await conn.execute(
                select(conversations.c.id, conversations.c.system_prompt)
                .where(conversations.c.user_id == user_id)
                .order_by(conversations.c.created_at.desc())
                .limit(1)
            )
            row = result.first()

            if row:
                conversation_id = row[0]
                logger.debug(f"Найден существующий контекст для user {user_id}")
            else:
                # Создаем новый диалог
                result = await conn.execute(
                    insert(conversations)
                    .values(
                        user_id=user_id,
                        system_prompt=system_prompt,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                    )
                    .returning(conversations.c.id)
                )
                conversation_id = result.scalar_one()
                logger.debug(f"Создан новый контекст для user {user_id}")

            # Загружаем сообщения (не удаленные, последние max_history)
            messages_result = await conn.execute(
                select(
                    user_messages.c.id,
                    user_messages.c.user_id,
                    user_messages.c.text,
                    user_messages.c.timestamp,
                    user_messages.c.content_length,
                    user_messages.c.is_deleted,
                )
                .where(
                    and_(
                        user_messages.c.conversation_id == conversation_id,
                        user_messages.c.is_deleted == False,  # noqa: E712
                    )
                )
                .order_by(user_messages.c.timestamp.desc())
                .limit(self.max_history)
            )
            messages_rows = messages_result.all()

            # Загружаем ответы (не удаленные, последние max_history)
            responses_result = await conn.execute(
                select(
                    llm_responses.c.id,
                    llm_responses.c.content,
                    llm_responses.c.timestamp,
                    llm_responses.c.model_used,
                    llm_responses.c.content_length,
                    llm_responses.c.is_deleted,
                )
                .where(
                    and_(
                        llm_responses.c.conversation_id == conversation_id,
                        llm_responses.c.is_deleted == False,  # noqa: E712
                    )
                )
                .order_by(llm_responses.c.timestamp.desc())
                .limit(self.max_history)
            )
            responses_rows = responses_result.all()

        # Преобразуем в модели (в обратном порядке для сохранения хронологии)
        messages = [
            UserMessage(
                id=row[0],
                user_id=row[1],
                text=row[2],
                timestamp=row[3],
                is_deleted=row[5],
            )
            for row in reversed(messages_rows)
        ]

        responses = [
            LLMResponse(
                id=row[0],
                content=row[1],
                timestamp=row[2],
                model_used=row[3],
                is_deleted=row[5],
            )
            for row in reversed(responses_rows)
        ]

        return ConversationContext(
            user_id=user_id,
            messages=messages,
            responses=responses,
            system_prompt=system_prompt,
        )

    async def add_message(self, user_id: int, text: str, system_prompt: str) -> None:
        """
        Добавить сообщение пользователя

        Args:
            user_id: ID пользователя
            text: Текст сообщения
            system_prompt: Системный промпт
        """
        async with self.engine.begin() as conn:
            # Получаем или создаем conversation_id
            result = await conn.execute(
                select(conversations.c.id)
                .where(conversations.c.user_id == user_id)
                .order_by(conversations.c.created_at.desc())
                .limit(1)
            )
            row = result.first()

            if row:
                conversation_id = row[0]
                # Обновляем updated_at
                await conn.execute(
                    update(conversations)
                    .where(conversations.c.id == conversation_id)
                    .values(updated_at=datetime.now())
                )
            else:
                # Создаем новый диалог
                result = await conn.execute(
                    insert(conversations)
                    .values(
                        user_id=user_id,
                        system_prompt=system_prompt,
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                    )
                    .returning(conversations.c.id)
                )
                conversation_id = result.scalar_one()

            # Добавляем сообщение
            content_length = len(text)
            await conn.execute(
                insert(user_messages).values(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    text=text,
                    content_length=content_length,
                    timestamp=datetime.now(),
                    is_deleted=False,
                )
            )

        logger.info(f"Добавлено сообщение от user {user_id} ({content_length} символов)")
        await self._trim_history(user_id)

    async def add_response(self, user_id: int, content: str, model: str) -> None:
        """
        Добавить ответ LLM

        Args:
            user_id: ID пользователя
            content: Содержимое ответа
            model: Модель LLM
        """
        async with self.engine.begin() as conn:
            # Получаем conversation_id
            result = await conn.execute(
                select(conversations.c.id)
                .where(conversations.c.user_id == user_id)
                .order_by(conversations.c.created_at.desc())
                .limit(1)
            )
            row = result.first()

            if not row:
                logger.warning(f"Попытка добавить ответ для несуществующего user {user_id}")
                return

            conversation_id = row[0]

            # Обновляем updated_at
            await conn.execute(
                update(conversations)
                .where(conversations.c.id == conversation_id)
                .values(updated_at=datetime.now())
            )

            # Добавляем ответ
            content_length = len(content)
            await conn.execute(
                insert(llm_responses).values(
                    conversation_id=conversation_id,
                    content=content,
                    content_length=content_length,
                    model_used=model,
                    timestamp=datetime.now(),
                    is_deleted=False,
                )
            )

        logger.info(f"Добавлен ответ для user {user_id} ({content_length} символов)")
        await self._trim_history(user_id)

    async def get_context(self, user_id: int) -> ConversationContext | None:
        """
        Получить контекст пользователя

        Args:
            user_id: ID пользователя

        Returns:
            Контекст диалога или None
        """
        async with self.engine.begin() as conn:
            # Проверяем, есть ли диалог
            result = await conn.execute(
                select(conversations.c.system_prompt)
                .where(conversations.c.user_id == user_id)
                .order_by(conversations.c.created_at.desc())
                .limit(1)
            )
            row = result.first()

            if not row:
                return None

            system_prompt = row[0]

        # Используем get_or_create_context для загрузки полного контекста
        return await self.get_or_create_context(user_id, system_prompt)

    async def clear(self, user_id: int) -> None:
        """
        Очистить историю пользователя (soft delete)

        Args:
            user_id: ID пользователя
        """
        async with self.engine.begin() as conn:
            # Получаем conversation_id
            result = await conn.execute(
                select(conversations.c.id)
                .where(conversations.c.user_id == user_id)
                .order_by(conversations.c.created_at.desc())
                .limit(1)
            )
            row = result.first()

            if not row:
                return

            conversation_id = row[0]

            # Soft delete всех сообщений
            await conn.execute(
                update(user_messages)
                .where(user_messages.c.conversation_id == conversation_id)
                .values(is_deleted=True)
            )

            # Soft delete всех ответов
            await conn.execute(
                update(llm_responses)
                .where(llm_responses.c.conversation_id == conversation_id)
                .values(is_deleted=True)
            )

        logger.info(f"История для user {user_id} очищена (soft delete)")

    async def _trim_history(self, user_id: int) -> None:
        """
        Ограничить историю до max_history (soft delete старых записей)

        Args:
            user_id: ID пользователя
        """
        async with self.engine.begin() as conn:
            # Получаем conversation_id
            result = await conn.execute(
                select(conversations.c.id)
                .where(conversations.c.user_id == user_id)
                .order_by(conversations.c.created_at.desc())
                .limit(1)
            )
            row = result.first()

            if not row:
                return

            conversation_id = row[0]

            # Находим ID старых сообщений (оставляем последние max_history)
            messages_result = await conn.execute(
                select(user_messages.c.id)
                .where(
                    and_(
                        user_messages.c.conversation_id == conversation_id,
                        user_messages.c.is_deleted == False,  # noqa: E712
                    )
                )
                .order_by(user_messages.c.timestamp.desc())
                .offset(self.max_history)
            )
            old_message_ids = [row[0] for row in messages_result.all()]

            if old_message_ids:
                await conn.execute(
                    update(user_messages)
                    .where(user_messages.c.id.in_(old_message_ids))
                    .values(is_deleted=True)
                )

            # Находим ID старых ответов
            responses_result = await conn.execute(
                select(llm_responses.c.id)
                .where(
                    and_(
                        llm_responses.c.conversation_id == conversation_id,
                        llm_responses.c.is_deleted == False,  # noqa: E712
                    )
                )
                .order_by(llm_responses.c.timestamp.desc())
                .offset(self.max_history)
            )
            old_response_ids = [row[0] for row in responses_result.all()]

            if old_response_ids:
                await conn.execute(
                    update(llm_responses)
                    .where(llm_responses.c.id.in_(old_response_ids))
                    .values(is_deleted=True)
                )

            if old_message_ids or old_response_ids:
                logger.debug(
                    f"История user {user_id} обрезана: "
                    f"{len(old_message_ids)} сообщений, "
                    f"{len(old_response_ids)} ответов помечены как удаленные"
                )
