"""Интерфейс для сборщика статистики"""

from abc import ABC, abstractmethod

from .models import DashboardStats


class StatCollector(ABC):
    """
    Абстрактный базовый класс для сборщиков статистики дашборда

    Определяет интерфейс для получения статистики диалогов.
    Может иметь различные реализации: Mock, Database-based и т.д.
    """

    @abstractmethod
    async def get_stats(self, period: str) -> DashboardStats:
        """
        Получить статистику за указанный период

        Args:
            period: Период для статистики ('day', 'week', 'month')

        Returns:
            Полная статистика для дашборда

        Raises:
            ValueError: Если передан некорректный период
        """
        pass
