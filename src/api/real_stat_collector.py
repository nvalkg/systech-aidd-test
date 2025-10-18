"""Реальный сборщик статистики из базы данных"""

import logging
from datetime import datetime, timedelta

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from ..database import conversations, user_messages
from .models import (
    ConversationItem,
    DashboardStats,
    MetricCard,
    TimeSeriesPoint,
    TopUser,
)
from .stat_collector import StatCollector

logger = logging.getLogger(__name__)


class RealStatCollector(StatCollector):
    """
    Реальный сборщик статистики из PostgreSQL базы данных

    Собирает статистику диалогов из таблиц conversations, user_messages, llm_responses.
    """

    def __init__(self, engine: AsyncEngine) -> None:
        """
        Инициализация Real сборщика

        Args:
            engine: Асинхронный движок SQLAlchemy для подключения к БД
        """
        self.engine = engine
        logger.info("RealStatCollector инициализирован")

    async def get_stats(self, period: str) -> DashboardStats:
        """
        Получить реальную статистику за период из БД

        Args:
            period: Период ('day', 'week', 'month')

        Returns:
            Статистика для дашборда с реальными данными

        Raises:
            ValueError: Если передан некорректный период
        """
        if period not in ["day", "week", "month"]:
            raise ValueError(f"Invalid period: {period}. Must be 'day', 'week', or 'month'")

        logger.info(f"Сбор статистики за период: {period}")

        # Определяем временные границы периода
        now = datetime.now()
        period_start = self._get_period_start(now, period)
        prev_period_start = self._get_period_start(period_start, period)

        async with self.engine.begin() as conn:
            # Собираем все метрики параллельно
            metrics = await self._generate_metrics(conn, period, period_start, prev_period_start)
            activity_chart = await self._generate_activity_chart(conn, period, period_start)
            recent_conversations = await self._generate_recent_conversations(conn)
            top_users = await self._generate_top_users(conn)

        return DashboardStats(
            metrics=metrics,
            activity_chart=activity_chart,
            recent_conversations=recent_conversations,
            top_users=top_users,
            period=period,
        )

    def _get_period_start(self, reference_time: datetime, period: str) -> datetime:
        """Получить начало периода относительно reference_time"""
        if period == "day":
            return reference_time - timedelta(days=1)
        elif period == "week":
            return reference_time - timedelta(weeks=1)
        else:  # month
            return reference_time - timedelta(days=30)

    async def _generate_metrics(
        self,
        conn: AsyncConnection,
        period: str,
        period_start: datetime,
        prev_period_start: datetime,
    ) -> list[MetricCard]:
        """Генерация 4 карточек метрик из реальных данных"""

        # 1. Total Conversations за период
        result = await conn.execute(
            select(func.count(conversations.c.id)).where(conversations.c.created_at >= period_start)
        )
        total_conv_current = result.scalar() or 0

        result = await conn.execute(
            select(func.count(conversations.c.id)).where(
                and_(
                    conversations.c.created_at >= prev_period_start,
                    conversations.c.created_at < period_start,
                )
            )
        )
        total_conv_prev = result.scalar() or 1  # избегаем деления на 0

        total_conv_trend = ((total_conv_current - total_conv_prev) / total_conv_prev) * 100

        # 2. New Users за период
        result = await conn.execute(
            select(func.count(func.distinct(conversations.c.user_id))).where(
                conversations.c.created_at >= period_start
            )
        )
        new_users_current = result.scalar() or 0

        result = await conn.execute(
            select(func.count(func.distinct(conversations.c.user_id))).where(
                and_(
                    conversations.c.created_at >= prev_period_start,
                    conversations.c.created_at < period_start,
                )
            )
        )
        new_users_prev = result.scalar() or 1

        new_users_trend = ((new_users_current - new_users_prev) / new_users_prev) * 100

        # 3. Active Conversations (с сообщениями за период)
        result = await conn.execute(
            select(func.count(func.distinct(user_messages.c.conversation_id))).where(
                and_(
                    user_messages.c.timestamp >= period_start,
                    user_messages.c.is_deleted == False,  # noqa: E712
                )
            )
        )
        active_conv_current = result.scalar() or 0

        result = await conn.execute(
            select(func.count(func.distinct(user_messages.c.conversation_id))).where(
                and_(
                    user_messages.c.timestamp >= prev_period_start,
                    user_messages.c.timestamp < period_start,
                    user_messages.c.is_deleted == False,  # noqa: E712
                )
            )
        )
        active_conv_prev = result.scalar() or 1

        active_conv_trend = ((active_conv_current - active_conv_prev) / active_conv_prev) * 100

        # 4. Avg Messages per Conversation
        result = await conn.execute(
            select(
                func.count(user_messages.c.id),
                func.count(func.distinct(user_messages.c.conversation_id)),
            ).where(
                and_(
                    user_messages.c.timestamp >= period_start,
                    user_messages.c.is_deleted == False,  # noqa: E712
                )
            )
        )
        row = result.first()
        total_messages_current = row[0] if row else 0
        total_conversations_current = row[1] if row else 1
        avg_messages_current = total_messages_current / total_conversations_current

        result = await conn.execute(
            select(
                func.count(user_messages.c.id),
                func.count(func.distinct(user_messages.c.conversation_id)),
            ).where(
                and_(
                    user_messages.c.timestamp >= prev_period_start,
                    user_messages.c.timestamp < period_start,
                    user_messages.c.is_deleted == False,  # noqa: E712
                )
            )
        )
        row = result.first()
        total_messages_prev = row[0] if row else 0
        total_conversations_prev = row[1] if row else 1
        avg_messages_prev = total_messages_prev / total_conversations_prev or 1

        avg_messages_trend = ((avg_messages_current - avg_messages_prev) / avg_messages_prev) * 100

        return [
            MetricCard(
                title="Total Conversations",
                value=f"{total_conv_current:,}",
                trend=round(total_conv_trend, 1),
                trend_label=self._get_trend_label(total_conv_trend, period),
                description=f"Total conversations in the last {period}",
            ),
            MetricCard(
                title="New Users",
                value=f"{new_users_current:,}",
                trend=round(new_users_trend, 1),
                trend_label=self._get_trend_label(new_users_trend, period),
                description=f"New users who started conversations this {period}",
            ),
            MetricCard(
                title="Active Conversations",
                value=f"{active_conv_current:,}",
                trend=round(active_conv_trend, 1),
                trend_label=self._get_trend_label(active_conv_trend, period),
                description=f"Conversations with activity in {period}",
            ),
            MetricCard(
                title="Avg Messages per Conversation",
                value=f"{avg_messages_current:.1f}",
                trend=round(avg_messages_trend, 1),
                trend_label=self._get_trend_label(avg_messages_trend, period),
                description="Average user messages per conversation",
            ),
        ]

    def _get_trend_label(self, trend: float, period: str) -> str:
        """Генерация текстовой метки для тренда"""
        if trend > 10:
            return f"Strong growth this {period}"
        elif trend > 0:
            return f"Trending up this {period}"
        elif trend > -10:
            return f"Slightly down from last {period}"
        else:
            return f"Significant decline this {period}"

    async def _generate_activity_chart(
        self, conn: AsyncConnection, period: str, period_start: datetime
    ) -> list[TimeSeriesPoint]:
        """Генерация данных для графика активности из реальных сообщений"""
        points = []

        if period == "day":
            # Почасовая статистика (24 точки)
            truncate_func = "hour"
            num_points = 24
        elif period == "week":
            # Посуточная статистика (7 точек)
            truncate_func = "day"
            num_points = 7
        else:  # month
            # Посуточная статистика (30 точек)
            truncate_func = "day"
            num_points = 30

        # SQL запрос с группировкой по временным интервалам
        result = await conn.execute(
            select(
                func.date_trunc(truncate_func, user_messages.c.timestamp).label("time_bucket"),
                func.count(user_messages.c.id).label("message_count"),
            )
            .where(
                and_(
                    user_messages.c.timestamp >= period_start,
                    user_messages.c.is_deleted == False,  # noqa: E712
                )
            )
            .group_by("time_bucket")
            .order_by("time_bucket")
        )

        # Создаем словарь для быстрого доступа к данным
        data_map = {row[0]: row[1] for row in result.all()}

        # Заполняем все точки (включая пустые)
        now = datetime.now()
        for i in range(num_points):
            if period == "day":
                timestamp = now - timedelta(hours=(num_points - 1 - i))
                timestamp = timestamp.replace(minute=0, second=0, microsecond=0)
            else:  # week or month
                timestamp = now - timedelta(days=(num_points - 1 - i))
                timestamp = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)

            # Получаем значение из БД или 0
            value = data_map.get(timestamp, 0)

            points.append(
                TimeSeriesPoint(
                    timestamp=timestamp.isoformat() + "Z",
                    value=value,
                )
            )

        return points

    async def _generate_recent_conversations(self, conn: AsyncConnection) -> list[ConversationItem]:
        """Генерация списка последних 10 диалогов"""
        # Запрос последних 10 диалогов с количеством сообщений
        result = await conn.execute(
            select(
                conversations.c.id,
                conversations.c.user_id,
                conversations.c.created_at,
                conversations.c.updated_at,
                func.count(user_messages.c.id).label("messages_count"),
            )
            .outerjoin(
                user_messages,
                and_(
                    user_messages.c.conversation_id == conversations.c.id,
                    user_messages.c.is_deleted == False,  # noqa: E712
                ),
            )
            .group_by(
                conversations.c.id,
                conversations.c.user_id,
                conversations.c.created_at,
                conversations.c.updated_at,
            )
            .order_by(conversations.c.updated_at.desc())
            .limit(10)
        )

        items = []
        for row in result.all():
            items.append(
                ConversationItem(
                    conversation_id=row[0],
                    user_id=row[1],
                    messages_count=row[4],
                    last_activity=row[3].isoformat() + "Z",
                    created_at=row[2].isoformat() + "Z",
                )
            )

        return items

    async def _generate_top_users(self, conn: AsyncConnection) -> list[TopUser]:
        """Генерация топ 5 пользователей по активности"""
        result = await conn.execute(
            select(
                user_messages.c.user_id,
                func.count(user_messages.c.id).label("messages_count"),
                func.count(func.distinct(user_messages.c.conversation_id)).label(
                    "conversations_count"
                ),
            )
            .where(user_messages.c.is_deleted == False)  # noqa: E712
            .group_by(user_messages.c.user_id)
            .order_by(func.count(user_messages.c.id).desc())
            .limit(5)
        )

        top_users = []
        for row in result.all():
            top_users.append(
                TopUser(
                    user_id=row[0],
                    messages_count=row[1],
                    conversations_count=row[2],
                )
            )

        return top_users
