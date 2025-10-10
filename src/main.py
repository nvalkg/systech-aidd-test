"""Точка входа приложения"""
import logging
from config import Config


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def main():
    """Тестирование загрузки конфигурации"""
    try:
        logger.info("Запуск приложения...")
        
        config = Config()
        logger.info("✅ Конфигурация успешно загружена")
        logger.info(f"Модель: {config.default_model}")
        logger.info(f"Max tokens: {config.max_tokens}")
        logger.info(f"Temperature: {config.temperature}")
        logger.info(f"Max history: {config.max_history_messages}")
        logger.info(f"Log level: {config.log_level}")
        logger.info(f"System prompt: {config.system_prompt[:50]}...")
        
    except ValueError as e:
        logger.error(f"❌ Ошибка конфигурации: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка: {e}")
        exit(1)


if __name__ == "__main__":
    main()

