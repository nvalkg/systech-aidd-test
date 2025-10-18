"""Mock реализация сборщика статистики для разработки frontend"""

import random
from datetime import datetime, timedelta

from .models import (
    ConversationItem,
    DashboardStats,
    MetricCard,
    TimeSeriesPoint,
    TopUser,
)
from .stat_collector import StatCollector


class MockStatCollector(StatCollector):
    """
    Mock реализация сборщика статистики с генерацией тестовых данных

    Генерирует реалистичные данные для разработки и тестирования frontend.
    Использует фиксированный seed для консистентности данных между запросами.
    """

    def __init__(self, seed: int = 42) -> None:
        """
        Инициализация Mock сборщика

        Args:
            seed: Seed для генератора случайных чисел (для консистентности данных)
        """
        self.seed = seed

    async def get_stats(self, period: str) -> DashboardStats:
        """
        Получить mock статистику за период

        Args:
            period: Период ('day', 'week', 'month')

        Returns:
            Статистика для дашборда с тестовыми данными

        Raises:
            ValueError: Если передан некорректный период
        """
        if period not in ["day", "week", "month"]:
            raise ValueError(f"Invalid period: {period}. Must be 'day', 'week', or 'month'")

        # Используем seed на основе периода для разных данных
        random.seed(self.seed + hash(period))

        # Генерируем данные в зависимости от периода
        metrics = self._generate_metrics(period)
        activity_chart = self._generate_activity_chart(period)
        recent_conversations = self._generate_recent_conversations()
        top_users = self._generate_top_users()

        return DashboardStats(
            metrics=metrics,
            activity_chart=activity_chart,
            recent_conversations=recent_conversations,
            top_users=top_users,
            period=period,
        )

    def _generate_metrics(self, period: str) -> list[MetricCard]:
        """Генерация 4 карточек метрик"""
        # Базовые значения зависят от периода
        period_multipliers = {"day": 1, "week": 7, "month": 30}
        multiplier = period_multipliers[period]

        # Total Conversations
        total_conv_value = random.randint(800, 1500) * multiplier
        total_conv_trend = random.uniform(-5, 20)

        # New Users
        new_users_value = random.randint(50, 200) * multiplier
        new_users_trend = random.uniform(-15, 25)

        # Active Conversations
        active_conv_value = random.randint(30000, 50000) * multiplier
        active_conv_trend = random.uniform(5, 20)

        # Average Messages
        avg_messages_value = random.uniform(3.5, 6.5)
        avg_messages_trend = random.uniform(-3, 8)

        return [
            MetricCard(
                title="Total Conversations",
                value=f"{total_conv_value:,}",
                trend=round(total_conv_trend, 1),
                trend_label=self._get_trend_label(total_conv_trend, period),
                description=f"Total conversations in the last {period}",
            ),
            MetricCard(
                title="New Users",
                value=f"{new_users_value:,}",
                trend=round(new_users_trend, 1),
                trend_label=self._get_trend_label(new_users_trend, period),
                description=f"New users who started conversations this {period}",
            ),
            MetricCard(
                title="Active Conversations",
                value=f"{active_conv_value:,}",
                trend=round(active_conv_trend, 1),
                trend_label=self._get_trend_label(active_conv_trend, period),
                description=f"Conversations with activity in {period}",
            ),
            MetricCard(
                title="Avg Messages per Conversation",
                value=f"{avg_messages_value:.1f}",
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

    def _generate_activity_chart(self, period: str) -> list[TimeSeriesPoint]:
        """Генерация данных для графика активности"""
        now = datetime.now()
        points = []

        if period == "day":
            # Почасовая статистика (24 точки)
            for i in range(24):
                timestamp = now - timedelta(hours=23 - i)
                # Имитируем суточный паттерн активности
                hour = timestamp.hour
                base_activity = 100
                if 9 <= hour <= 18:  # Рабочие часы
                    base_activity = 200
                elif 0 <= hour <= 6:  # Ночь
                    base_activity = 50

                value = base_activity + random.randint(-30, 50)
                points.append(
                    TimeSeriesPoint(
                        timestamp=timestamp.replace(minute=0, second=0).isoformat() + "Z",
                        value=value,
                    )
                )

        elif period == "week":
            # Посуточная статистика (7 точек)
            for i in range(7):
                timestamp = now - timedelta(days=6 - i)
                # Имитируем недельный паттерн (будни активнее выходных)
                weekday = timestamp.weekday()
                base_activity = 150 if weekday < 5 else 100

                value = base_activity + random.randint(-20, 80)
                points.append(
                    TimeSeriesPoint(
                        timestamp=timestamp.replace(hour=0, minute=0, second=0).isoformat() + "Z",
                        value=value,
                    )
                )

        else:  # month
            # Посуточная статистика (30 точек)
            for i in range(30):
                timestamp = now - timedelta(days=29 - i)
                # Общий растущий тренд с флуктуациями
                trend = i * 2
                base_activity = 120 + trend

                value = base_activity + random.randint(-30, 50)
                points.append(
                    TimeSeriesPoint(
                        timestamp=timestamp.replace(hour=0, minute=0, second=0).isoformat() + "Z",
                        value=value,
                    )
                )

        return points

    def _generate_recent_conversations(self) -> list[ConversationItem]:
        """Генерация списка последних 10 диалогов"""
        now = datetime.now()
        conversations = []

        for i in range(10):
            conversation_id = 2000 - i
            user_id = random.randint(100000000, 999999999)
            messages_count = random.randint(2, 25)

            # Последняя активность в пределах последних часов/дней
            hours_ago = i * 2 + random.randint(0, 3)
            last_activity = now - timedelta(hours=hours_ago)

            # Создание диалога раньше последней активности
            created_hours_ago = hours_ago + random.randint(1, 48)
            created_at = now - timedelta(hours=created_hours_ago)

            conversations.append(
                ConversationItem(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    messages_count=messages_count,
                    last_activity=last_activity.isoformat() + "Z",
                    created_at=created_at.isoformat() + "Z",
                )
            )

        return conversations

    def _generate_top_users(self) -> list[TopUser]:
        """Генерация топ 5 пользователей по активности"""
        top_users = []

        # Первый пользователь - самый активный
        base_messages = random.randint(200, 300)

        for i in range(5):
            user_id = random.randint(100000000, 999999999)
            # Убывающее количество сообщений
            messages_count = base_messages - i * random.randint(15, 30)
            # Разное количество диалогов
            conversations_count = random.randint(3, 15)

            top_users.append(
                TopUser(
                    user_id=user_id,
                    messages_count=messages_count,
                    conversations_count=conversations_count,
                )
            )

        return top_users
