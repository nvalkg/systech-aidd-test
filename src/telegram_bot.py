"""Telegram бот для работы с пользователями"""
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from conversation_manager import ConversationManager


logger = logging.getLogger(__name__)


class TelegramBot:
    """Telegram бот с полной интеграцией LLM"""
    
    def __init__(self, token: str, conversation_manager: ConversationManager):
        """
        Инициализация Telegram бота
        
        Args:
            token: Токен бота от BotFather
            conversation_manager: Менеджер диалогов
        """
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.conversation_manager = conversation_manager
        
        # Регистрация обработчиков
        self.dp.message.register(self.cmd_start, Command("start"))
        self.dp.message.register(self.handle_message)  # Обработка всех текстовых сообщений
        
        logger.info("TelegramBot инициализирован с ConversationManager")
    
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
    
    async def handle_message(self, message: Message):
        """
        Обработчик текстовых сообщений
        
        Args:
            message: Сообщение от пользователя
        """
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name
        text = message.text
        
        # Игнорируем пустые сообщения
        if not text or not text.strip():
            logger.info(f"Игнорируем пустое сообщение от user {user_id}")
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
            error_message = "Извините, произошла ошибка при обработке вашего сообщения. Попробуйте позже."
            await message.answer(error_message)
    
    async def start_polling(self):
        """Запуск бота в режиме polling"""
        logger.info("Запуск polling...")
        await self.dp.start_polling(self.bot)
    
    async def stop(self):
        """Остановка бота"""
        logger.info("Остановка бота...")
        await self.bot.session.close()

