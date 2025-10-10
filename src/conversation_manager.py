"""Управление контекстом диалога"""
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from llm_client import LLMClient


logger = logging.getLogger(__name__)


@dataclass
class UserMessage:
    """Сообщение пользователя"""
    user_id: int
    text: str
    timestamp: datetime


@dataclass
class LLMResponse:
    """Ответ LLM"""
    content: str
    timestamp: datetime
    model_used: str


@dataclass
class ConversationContext:
    """Контекст диалога"""
    user_id: int
    messages: List[UserMessage]
    responses: List[LLMResponse]
    system_prompt: str


class ConversationManager:
    """Управление диалогом с пользователем"""
    
    def __init__(self, llm_client: LLMClient, system_prompt: str, max_history: int = 10):
        """
        Инициализация менеджера диалога
        
        Args:
            llm_client: Клиент для работы с LLM
            system_prompt: Системный промпт для LLM
            max_history: Максимальное количество сообщений в истории
        """
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self.max_history = max_history
        self.contexts: Dict[int, ConversationContext] = {}
        
        logger.info(f"ConversationManager инициализирован (max_history={max_history})")
    
    def add_user_message(self, user_id: int, text: str):
        """Добавить сообщение пользователя"""
        if user_id not in self.contexts:
            self.contexts[user_id] = ConversationContext(
                user_id=user_id,
                messages=[],
                responses=[],
                system_prompt=self.system_prompt
            )
        
        message = UserMessage(
            user_id=user_id,
            text=text,
            timestamp=datetime.now()
        )
        
        self.contexts[user_id].messages.append(message)
        self._trim_history(user_id)
        
        logger.info(f"Добавлено сообщение от user {user_id} ({len(text)} символов)")
    
    def add_llm_response(self, user_id: int, content: str, model: str):
        """Добавить ответ LLM"""
        if user_id not in self.contexts:
            return
        
        response = LLMResponse(
            content=content,
            timestamp=datetime.now(),
            model_used=model
        )
        
        self.contexts[user_id].responses.append(response)
        self._trim_history(user_id)
        
        logger.info(f"Добавлен ответ для user {user_id} ({len(content)} символов)")
    
    def get_messages_for_llm(self, user_id: int) -> List[Dict[str, str]]:
        """
        Получить сообщения в формате для LLM API
        
        Returns:
            Список сообщений [{"role": "...", "content": "..."}]
        """
        if user_id not in self.contexts:
            return [{"role": "system", "content": self.system_prompt}]
        
        context = self.contexts[user_id]
        messages = [{"role": "system", "content": context.system_prompt}]
        
        # Чередуем user и assistant сообщения
        for i in range(min(len(context.messages), len(context.responses))):
            messages.append({"role": "user", "content": context.messages[i].text})
            messages.append({"role": "assistant", "content": context.responses[i].content})
        
        # Если есть непарное сообщение пользователя
        if len(context.messages) > len(context.responses):
            messages.append({"role": "user", "content": context.messages[-1].text})
        
        return messages
    
    async def process_message(self, user_id: int, text: str) -> str:
        """
        Обработать сообщение пользователя и получить ответ
        
        Args:
            user_id: ID пользователя
            text: Текст сообщения
            
        Returns:
            Ответ от LLM
        """
        self.add_user_message(user_id, text)
        messages = self.get_messages_for_llm(user_id)
        
        response = await self.llm_client.get_response(messages)
        self.add_llm_response(user_id, response, self.llm_client.model)
        
        return response
    
    def clear_history(self, user_id: int):
        """Очистить историю диалога пользователя"""
        if user_id in self.contexts:
            del self.contexts[user_id]
            logger.info(f"История диалога для user {user_id} очищена")
    
    def _trim_history(self, user_id: int):
        """Ограничить историю до max_history сообщений"""
        context = self.contexts[user_id]
        
        if len(context.messages) > self.max_history:
            context.messages = context.messages[-self.max_history:]
            context.responses = context.responses[-self.max_history:]
            logger.debug(f"История user {user_id} обрезана до {self.max_history} сообщений")

