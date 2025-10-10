"""Клиент для работы с LLM через OpenRouter"""
import logging
from typing import List, Dict
from openai import AsyncOpenAI


logger = logging.getLogger(__name__)


class LLMClient:
    """Клиент для взаимодействия с OpenRouter API"""
    
    def __init__(self, api_key: str, model: str, max_tokens: int, temperature: float):
        """
        Инициализация клиента OpenRouter
        
        Args:
            api_key: API ключ OpenRouter
            model: Название модели (например, openai/gpt-3.5-turbo)
            max_tokens: Максимальное количество токенов в ответе
            temperature: Температура генерации (0.0 - 1.0)
        """
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # Инициализация OpenAI клиента с base_url для OpenRouter
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        logger.info(f"LLMClient инициализирован: {model}")
    
    async def get_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Получить ответ от LLM
        
        Args:
            messages: Список сообщений в формате [{"role": "...", "content": "..."}]
            
        Returns:
            Текст ответа от LLM
            
        Raises:
            Exception: При ошибках API
        """
        try:
            logger.info(f"Отправка запроса к {self.model} ({len(messages)} сообщений)")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
            
            logger.info(f"Получен ответ: {len(content)} символов, {tokens_used} токенов")
            
            return content
            
        except Exception as e:
            logger.error(f"Ошибка при запросе к LLM: {e}")
            raise

