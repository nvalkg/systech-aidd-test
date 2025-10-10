"""Точка входа приложения"""
import logging
import asyncio
from config import Config
from llm_client import LLMClient


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


async def test_llm_client():
    """Тестирование LLM клиента"""
    try:
        logger.info("=== Тест LLM Client ===")
        
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
        
        # Тестовый запрос
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello, World!' in one sentence."}
        ]
        
        logger.info("Отправка тестового запроса...")
        response = await llm_client.get_response(test_messages)
        
        logger.info(f"✅ Ответ получен: {response}")
        
    except ValueError as e:
        logger.error(f"❌ Ошибка конфигурации: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        exit(1)


def main():
    """Запуск тестирования"""
    asyncio.run(test_llm_client())


if __name__ == "__main__":
    main()

