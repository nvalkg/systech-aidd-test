"""Точка входа приложения"""
import logging
import asyncio
from config import Config
from llm_client import LLMClient
from conversation_manager import ConversationManager


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


async def test_conversation_manager():
    """Тестирование ConversationManager"""
    try:
        logger.info("=== Тест Conversation Manager ===")
        
        # Загрузка конфигурации
        config = Config()
        logger.info("✅ Конфигурация загружена")
        
        # Инициализация LLM клиента
        llm_client = LLMClient(
            api_key=config.openrouter_key,
            model=config.default_model,
            max_tokens=config.max_tokens,
            temperature=config.temperature
        )
        logger.info("✅ LLM клиент инициализирован")
        
        # Инициализация ConversationManager
        conversation_manager = ConversationManager(
            llm_client=llm_client,
            system_prompt=config.system_prompt,
            max_history=config.max_history_messages
        )
        logger.info("✅ ConversationManager инициализирован")
        
        # Тестовый диалог
        test_user_id = 12345
        
        logger.info("\n--- Сообщение 1 ---")
        response1 = await conversation_manager.process_message(
            test_user_id, 
            "Привет! Как тебя зовут?"
        )
        logger.info(f"Ответ 1: {response1}")
        
        logger.info("\n--- Сообщение 2 ---")
        response2 = await conversation_manager.process_message(
            test_user_id,
            "Какая сейчас погода в Москве?"
        )
        logger.info(f"Ответ 2: {response2}")
        
        logger.info("\n--- Сообщение 3 ---")
        response3 = await conversation_manager.process_message(
            test_user_id,
            "А что ты мне говорил о своем имени?"
        )
        logger.info(f"Ответ 3: {response3}")
        
        logger.info("\n✅ Тест завершен: диалог из 3 сообщений успешно обработан")
        
        # Тест очистки истории
        logger.info("\n--- Тест clear_history ---")
        conversation_manager.clear_history(test_user_id)
        logger.info("✅ История очищена")
        
    except ValueError as e:
        logger.error(f"❌ Ошибка конфигурации: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        exit(1)


def main():
    """Запуск тестирования"""
    asyncio.run(test_conversation_manager())


if __name__ == "__main__":
    main()

