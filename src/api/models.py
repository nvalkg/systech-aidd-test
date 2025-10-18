"""Модели данных для API статистики дашборда"""

from dataclasses import dataclass


@dataclass
class MetricCard:
    """
    Карточка метрики дашборда

    Attributes:
        title: Название метрики
        value: Текущее значение (отформатированная строка)
        trend: Процент изменения относительно предыдущего периода (может быть отрицательным)
        trend_label: Текстовое описание тренда
        description: Дополнительное описание метрики
    """

    title: str
    value: str
    trend: float
    trend_label: str
    description: str


@dataclass
class TimeSeriesPoint:
    """
    Точка временного ряда для графика активности

    Attributes:
        timestamp: Временная метка в ISO 8601 формате
        value: Значение метрики в этой точке
    """

    timestamp: str
    value: int


@dataclass
class ConversationItem:
    """
    Элемент списка диалогов

    Attributes:
        conversation_id: Идентификатор диалога
        user_id: Идентификатор пользователя
        messages_count: Количество сообщений в диалоге
        last_activity: Время последней активности в ISO 8601 формате
        created_at: Время создания диалога в ISO 8601 формате
    """

    conversation_id: int
    user_id: int
    messages_count: int
    last_activity: str
    created_at: str


@dataclass
class TopUser:
    """
    Пользователь в топе активности

    Attributes:
        user_id: Идентификатор пользователя
        messages_count: Общее количество отправленных сообщений
        conversations_count: Количество диалогов пользователя
    """

    user_id: int
    messages_count: int
    conversations_count: int


@dataclass
class DashboardStats:
    """
    Полная статистика для дашборда

    Attributes:
        metrics: Список из 4 карточек метрик
        activity_chart: Данные для графика активности (временной ряд)
        recent_conversations: Последние 10 диалогов
        top_users: Топ 5 пользователей по активности
        period: Выбранный период ('day', 'week', 'month')
    """

    metrics: list[MetricCard]
    activity_chart: list[TimeSeriesPoint]
    recent_conversations: list[ConversationItem]
    top_users: list[TopUser]
    period: str

    def __post_init__(self) -> None:
        """Валидация данных после инициализации"""
        if len(self.metrics) != 4:
            raise ValueError("Должно быть ровно 4 метрики")
        if self.period not in ["day", "week", "month"]:
            raise ValueError("Период должен быть 'day', 'week' или 'month'")
        if len(self.recent_conversations) > 10:
            raise ValueError("Максимум 10 последних диалогов")
        if len(self.top_users) > 5:
            raise ValueError("Максимум 5 топ пользователей")
