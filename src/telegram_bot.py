"""Telegram бот для работы с пользователями"""

import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from .conversation_manager import ConversationManager

logger = logging.getLogger(__name__)

# Константы для ограничений
MAX_MESSAGE_LENGTH = 4000

# Текстовые константы
WELCOME_TEXT = """👋 Привет! Я LLM-ассистент на основе GPT.

Я могу:
• Отвечать на твои вопросы
• Помогать с задачами
• Вести диалог с контекстом
• Запоминать предыдущие сообщения (до 10)

📝 Просто напиши мне сообщение, и я отвечу!

Доступные команды:
/help - справка по использованию
/clear - очистить историю диалога
/start - показать это сообщение"""

HELP_TEXT = """ℹ️ Справка по использованию

Как пользоваться ботом:
1. Просто напиши мне сообщение
2. Я отвечу с учетом контекста диалога
3. Бот помнит последние 10 сообщений

Доступные команды:
/start - приветствие и описание
/help - эта справка
/clear - очистить историю диалога

⚠️ Ограничения:
• Максимальная длина сообщения: 4000 символов
• Пустые сообщения игнорируются
• История сохраняется только в памяти

Если возникли проблемы, используй /clear и начни заново."""

CLEAR_TEXT = """🗑️ История диалога очищена!

Начнем общение с чистого листа. Напиши мне что-нибудь, и я отвечу."""

ERROR_MESSAGE_TOO_LONG = """⚠️ Сообщение слишком длинное ({length} символов).
Максимальная длина: {max_length} символов.

Пожалуйста, сократи сообщение и попробуй снова."""

ERROR_MESSAGE_GENERAL = """❌ Извините, произошла ошибка при обработке вашего сообщения.

Попробуйте:
• Переформулировать вопрос
• Использовать /clear для очистки истории
• Повторить попытку позже"""


class TelegramBot:
    """Telegram бот с полной интеграцией LLM"""

    def __init__(self, token: str, conversation_manager: ConversationManager) -> None:
        """
        Инициализация Telegram бота

        Args:
            token: Токен бота от BotFather
            conversation_manager: Менеджер диалогов
        """
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.conversation_manager = conversation_manager

        # Регистрация обработчиков команд
        self.dp.message.register(self.cmd_start, Command("start"))
        self.dp.message.register(self.cmd_help, Command("help"))
        self.dp.message.register(self.cmd_clear, Command("clear"))

        # Обработка всех текстовых сообщений (должен быть последним)
        self.dp.message.register(self.handle_message)

        logger.info("TelegramBot инициализирован с ConversationManager")

    def _get_user_info(self, message: Message) -> tuple[int, str]:
        """
        Безопасное извлечение информации о пользователе

        Args:
            message: Сообщение от пользователя

        Returns:
            Кортеж (user_id, username)

        Raises:
            ValueError: Если сообщение не содержит информации о пользователе
        """
        if not message.from_user:
            raise ValueError("Message has no user information")

        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name or "Unknown"
        return user_id, username

    async def cmd_start(self, message: Message) -> None:
        """
        Обработчик команды /start

        Args:
            message: Сообщение от пользователя
        """
        user_id, username = self._get_user_info(message)
        logger.info(f"Команда /start от user {user_id} (@{username})")

        await message.answer(WELCOME_TEXT)
        logger.info(f"Отправлено приветствие user {user_id}")

    async def cmd_help(self, message: Message) -> None:
        """
        Обработчик команды /help

        Args:
            message: Сообщение от пользователя
        """
        user_id, username = self._get_user_info(message)
        logger.info(f"Команда /help от user {user_id} (@{username})")

        await message.answer(HELP_TEXT)
        logger.info(f"Отправлена справка user {user_id}")

    async def cmd_clear(self, message: Message) -> None:
        """
        Обработчик команды /clear

        Args:
            message: Сообщение от пользователя
        """
        user_id, username = self._get_user_info(message)
        logger.info(f"Команда /clear от user {user_id} (@{username})")

        # Очистка истории диалога
        self.conversation_manager.clear_history(user_id)

        await message.answer(CLEAR_TEXT)
        logger.info(f"История очищена для user {user_id}")

    async def handle_message(self, message: Message) -> None:
        """
        Обработчик текстовых сообщений

        Args:
            message: Сообщение от пользователя
        """
        user_id, username = self._get_user_info(message)
        text = message.text

        # Игнорируем пустые сообщения
        if not text or not text.strip():
            logger.info(f"Игнорируем пустое сообщение от user {user_id}")
            return

        # Проверка длины сообщения
        if len(text) > MAX_MESSAGE_LENGTH:
            logger.warning(f"Слишком длинное сообщение от user {user_id}: {len(text)} символов")
            error_text = ERROR_MESSAGE_TOO_LONG.format(
                length=len(text), max_length=MAX_MESSAGE_LENGTH
            )
            await message.answer(error_text)
            return

        logger.info(f"Получено сообщение от user {user_id} (@{username}): {len(text)} символов")

        try:
            # Обработка сообщения через ConversationManager
            response = await self.conversation_manager.process_message(user_id, text)

            # Отправка ответа пользователю
            await message.answer(response)
            logger.info(f"Отправлен ответ user {user_id}: {len(response)} символов")

        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения от user {user_id}: {e}")
            await message.answer(ERROR_MESSAGE_GENERAL)

    async def start_polling(self) -> None:
        """Запуск бота в режиме polling"""
        logger.info("Запуск polling...")
        await self.dp.start_polling(self.bot)

    async def stop(self) -> None:
        """Остановка бота"""
        logger.info("Остановка бота...")
        await self.bot.session.close()
