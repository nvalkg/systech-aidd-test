"""Конфигурация приложения из переменных окружения"""
import os
from dotenv import load_dotenv


class Config:
    """Класс для загрузки и валидации конфигурации из .env файла"""
    
    def __init__(self):
        """Инициализация конфигурации с загрузкой переменных окружения"""
        load_dotenv()
        
        # Обязательные параметры
        self.telegram_token: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.openrouter_key: str = os.getenv('OPENROUTER_API_KEY', '')
        
        # Валидация обязательных токенов
        if not self.telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env файле")
        if not self.openrouter_key:
            raise ValueError("OPENROUTER_API_KEY не установлен в .env файле")
        
        # Необязательные параметры с значениями по умолчанию
        self.default_model: str = os.getenv('DEFAULT_MODEL', 'openai/gpt-3.5-turbo')
        self.max_tokens: int = int(os.getenv('MAX_TOKENS', '1000'))
        self.temperature: float = float(os.getenv('TEMPERATURE', '0.7'))
        self.max_history_messages: int = int(os.getenv('MAX_HISTORY_MESSAGES', '10'))
        self.system_prompt: str = os.getenv('SYSTEM_PROMPT', 'You are a helpful AI assistant.')
        self.log_level: str = os.getenv('LOG_LEVEL', 'INFO')

