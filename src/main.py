"""Точка входа приложения"""

import asyncio
import logging

from .config import Config
from .conversation_manager import ConversationManager
from .llm_client import LLMClient
from .telegram_bot import TelegramBot

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


async def main() -> None:
    """Запуск Telegram бота с полной интеграцией"""
    try:
        logger.info("=== Запуск LLM-ассистента ===")

        # Загрузка конфигурации
        config = Config()
        logger.info("✅ Конфигурация загружена")

        # Инициализация LLM клиента
        llm_client = LLMClient(
            api_key=config.openrouter_key,
            model=config.default_model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
        )
        logger.info("✅ LLM клиент инициализирован")

        # Инициализация ConversationManager
        conversation_manager = ConversationManager(
            llm_client=llm_client,
            system_prompt=config.system_prompt,
            max_history=config.max_history_messages,
        )
        logger.info("✅ ConversationManager инициализирован")

        # Инициализация Telegram бота
        telegram_bot = TelegramBot(
            token=config.telegram_token, conversation_manager=conversation_manager
        )
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
        if "telegram_bot" in locals():
            await telegram_bot.stop()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())
