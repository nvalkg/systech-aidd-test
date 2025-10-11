"""Telegram бот для работы с пользователями"""
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from conversation_manager import ConversationManager


logger = logging.getLogger(__name__)

# Константы для ограничений
MAX_MESSAGE_LENGTH = 4000


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
        
        # Регистрация обработчиков команд
        self.dp.message.register(self.cmd_start, Command("start"))
        self.dp.message.register(self.cmd_help, Command("help"))
        self.dp.message.register(self.cmd_clear, Command("clear"))
        
        # Обработка всех текстовых сообщений (должен быть последним)
        self.dp.message.register(self.handle_message)
        
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
            "👋 Привет! Я LLM-ассистент на основе GPT.\n\n"
            "Я могу:\n"
            "• Отвечать на твои вопросы\n"
            "• Помогать с задачами\n"
            "• Вести диалог с контекстом\n"
            "• Запоминать предыдущие сообщения (до 10)\n\n"
            "📝 Просто напиши мне сообщение, и я отвечу!\n\n"
            "Доступные команды:\n"
            "/help - справка по использованию\n"
            "/clear - очистить историю диалога\n"
            "/start - показать это сообщение"
        )
        
        await message.answer(welcome_text)
        logger.info(f"Отправлено приветствие user {user_id}")
    
    async def cmd_help(self, message: Message):
        """Обработчик команды /help"""
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name
        
        logger.info(f"Команда /help от user {user_id} (@{username})")
        
        help_text = (
            "ℹ️ Справка по использованию\n\n"
            "Как пользоваться ботом:\n"
            "1. Просто напиши мне сообщение\n"
            "2. Я отвечу с учетом контекста диалога\n"
            "3. Бот помнит последние 10 сообщений\n\n"
            "Доступные команды:\n"
            "/start - приветствие и описание\n"
            "/help - эта справка\n"
            "/clear - очистить историю диалога\n\n"
            "⚠️ Ограничения:\n"
            "• Максимальная длина сообщения: 4000 символов\n"
            "• Пустые сообщения игнорируются\n"
            "• История сохраняется только в памяти\n\n"
            "Если возникли проблемы, используй /clear и начни заново."
        )
        
        await message.answer(help_text)
        logger.info(f"Отправлена справка user {user_id}")
    
    async def cmd_clear(self, message: Message):
        """Обработчик команды /clear"""
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name
        
        logger.info(f"Команда /clear от user {user_id} (@{username})")
        
        # Очистка истории диалога
        self.conversation_manager.clear_history(user_id)
        
        clear_text = (
            "🗑️ История диалога очищена!\n\n"
            "Начнем общение с чистого листа. "
            "Напиши мне что-нибудь, и я отвечу."
        )
        
        await message.answer(clear_text)
        logger.info(f"История очищена для user {user_id}")
    
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
        
        # Проверка длины сообщения
        if len(text) > MAX_MESSAGE_LENGTH:
            logger.warning(f"Слишком длинное сообщение от user {user_id}: {len(text)} символов")
            error_text = (
                f"⚠️ Сообщение слишком длинное ({len(text)} символов).\n"
                f"Максимальная длина: {MAX_MESSAGE_LENGTH} символов.\n\n"
                "Пожалуйста, сократи сообщение и попробуй снова."
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
            error_message = (
                "❌ Извините, произошла ошибка при обработке вашего сообщения.\n\n"
                "Попробуйте:\n"
                "• Переформулировать вопрос\n"
                "• Использовать /clear для очистки истории\n"
                "• Повторить попытку позже"
            )
            await message.answer(error_message)
    
    async def start_polling(self):
        """Запуск бота в режиме polling"""
        logger.info("Запуск polling...")
        await self.dp.start_polling(self.bot)
    
    async def stop(self):
        """Остановка бота"""
        logger.info("Остановка бота...")
        await self.bot.session.close()

