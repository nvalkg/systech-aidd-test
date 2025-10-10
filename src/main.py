"""Точка входа приложения"""
import logging
import asyncio
from config import Config
from telegram_bot import TelegramBot


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


async def main():
    """Запуск Telegram бота"""
    try:
        logger.info("=== Запуск Telegram Bot ===")
        
        # Загрузка конфигурации
        config = Config()
        logger.info("✅ Конфигурация загружена")
        
        # Инициализация Telegram бота
        telegram_bot = TelegramBot(token=config.telegram_token)
        logger.info("✅ Telegram бот инициализирован")
        
        # Запуск polling
        logger.info("🚀 Бот запущен! Нажмите Ctrl+C для остановки")
        await telegram_bot.start_polling()
        
    except ValueError as e:
        logger.error(f"❌ Ошибка конфигурации: {e}")
        exit(1)
    except KeyboardInterrupt:
        logger.info("⏹️ Получен сигнал остановки")
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        exit(1)
    finally:
        if 'telegram_bot' in locals():
            await telegram_bot.stop()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())

