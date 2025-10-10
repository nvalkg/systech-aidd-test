"""Telegram бот для работы с пользователями"""
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


logger = logging.getLogger(__name__)


class TelegramBot:
    """Telegram бот с базовой функциональностью"""
    
    def __init__(self, token: str):
        """
        Инициализация Telegram бота
        
        Args:
            token: Токен бота от BotFather
        """
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        
        # Регистрация обработчиков
        self.dp.message.register(self.cmd_start, Command("start"))
        
        logger.info("TelegramBot инициализирован")
    
    async def cmd_start(self, message: Message):
        """
        Обработчик команды /start
        
        Args:
            message: Сообщение от пользователя
        """
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name
        
        logger.info(f"Команда /start от user {user_id} (@{username})")
        
        welcome_text = (
            "👋 Привет! Я LLM-ассистент.\n\n"
            "Я могу общаться с тобой на любые темы. "
            "Просто напиши мне сообщение, и я отвечу!\n\n"
            "Доступные команды:\n"
            "/start - это сообщение\n"
            "/help - справка\n"
            "/clear - очистить историю диалога"
        )
        
        await message.answer(welcome_text)
        logger.info(f"Отправлено приветствие user {user_id}")
    
    async def start_polling(self):
        """Запуск бота в режиме polling"""
        logger.info("Запуск polling...")
        await self.dp.start_polling(self.bot)
    
    async def stop(self):
        """Остановка бота"""
        logger.info("Остановка бота...")
        await self.bot.session.close()

