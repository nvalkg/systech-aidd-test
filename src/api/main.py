"""FastAPI приложение для Statistics API и Chat API"""

import logging
import os
from dataclasses import asdict

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..config import Config
from ..conversation_manager import ConversationManager
from ..database import create_engine
from ..db_history_storage import DatabaseHistoryStorage
from ..llm_client import LLMClient
from .mock_stat_collector import MockStatCollector
from .real_stat_collector import RealStatCollector
from .text2sql_manager import Text2SQLManager

logger = logging.getLogger(__name__)

app = FastAPI(
    title="AIDD API",
    description="API для статистики диалогов и веб-чата с LLM-ассистентом",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware для разработки frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production следует указать конкретные origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Глобальные переменные для менеджеров (инициализируются при старте)
collector = None
normal_conversation_manager = None
admin_conversation_manager = None
text2sql_manager = None


# Pydantic модели для Chat API
class ChatMessageRequest(BaseModel):
    session_id: str
    message: str
    mode: str = "normal"  # "normal" or "admin"


class ChatMessageResponse(BaseModel):
    response: str
    mode: str
    sql_query: str | None = None  # для admin mode


class ChatClearRequest(BaseModel):
    session_id: str


@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске приложения"""
    global collector, normal_conversation_manager, admin_conversation_manager, text2sql_manager

    logger.info("Инициализация AIDD API...")

    # Загружаем конфигурацию
    config = Config()

    # Создаем движок БД
    engine = create_engine(config.database_url)

    # Выбираем сборщик статистики (Mock или Real)
    use_mock = os.getenv("USE_MOCK_STATS", "false").lower() == "true"
    if use_mock:
        logger.info("Используется MockStatCollector для статистики")
        collector = MockStatCollector()
    else:
        logger.info("Используется RealStatCollector для статистики")
        collector = RealStatCollector(engine)

    # Инициализируем LLM клиент
    llm_client = LLMClient(
        api_key=config.openrouter_key,
        model=config.default_model,
        max_tokens=config.max_tokens,
        temperature=config.temperature,
    )

    # Инициализируем DatabaseHistoryStorage
    history_storage = DatabaseHistoryStorage(engine, max_history=config.max_history_messages)

    # Инициализируем Normal ConversationManager
    normal_conversation_manager = ConversationManager(
        llm_client=llm_client,
        system_prompt=config.system_prompt,
        storage=history_storage,
        max_history=config.max_history_messages,
    )
    logger.info("Normal ConversationManager инициализирован")

    # Загружаем text2sql промпт
    text2sql_prompt_path = "prompts/system_prompt_text2sql.txt"
    try:
        with open(text2sql_prompt_path, encoding="utf-8") as f:
            text2sql_prompt = f.read().strip()
    except FileNotFoundError:
        logger.warning(f"Файл {text2sql_prompt_path} не найден, используется упрощенный промпт")
        text2sql_prompt = "You are a SQL query generator. Generate only SELECT queries."

    # Инициализируем Text2SQLManager
    text2sql_manager = Text2SQLManager(
        llm_client=llm_client, engine=engine, text2sql_prompt=text2sql_prompt
    )
    logger.info("Text2SQLManager инициализирован")

    # Инициализируем Admin ConversationManager с отдельным storage
    admin_history_storage = DatabaseHistoryStorage(engine, max_history=config.max_history_messages)
    admin_conversation_manager = ConversationManager(
        llm_client=llm_client,
        system_prompt=text2sql_prompt,  # используем text2sql промпт как системный
        storage=admin_history_storage,
        max_history=config.max_history_messages,
    )
    logger.info("Admin ConversationManager инициализирован")

    logger.info("AIDD API успешно инициализирован")


@app.get("/")
async def root() -> dict[str, str]:
    """Корневой эндпоинт API"""
    return {
        "message": "AIDD Statistics API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/api/health")
async def health() -> dict[str, str]:
    """
    Health check endpoint

    Используется для проверки доступности API
    """
    return {"status": "ok"}


@app.get("/api/stats")
async def get_stats(
    period: str = Query(
        "week",
        description="Период для статистики",
        regex="^(day|week|month)$",
    ),
) -> dict:
    """
    Получить статистику дашборда за указанный период

    Args:
        period: Период для статистики ('day', 'week', 'month')

    Returns:
        Статистика дашборда в формате JSON

    Raises:
        HTTPException 400: Если передан некорректный период
        HTTPException 500: При внутренней ошибке сервера
    """
    try:
        stats = await collector.get_stats(period)
        # Конвертируем dataclass в dict для JSON сериализации
        return asdict(stats)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@app.post("/api/chat/message")
async def send_message(request: ChatMessageRequest) -> ChatMessageResponse:
    """
    Отправить сообщение в чат и получить ответ

    Args:
        request: Запрос с сообщением пользователя

    Returns:
        Ответ от LLM-ассистента

    Raises:
        HTTPException 500: При ошибке обработки сообщения
    """
    try:
        # Конвертируем session_id в user_id (hash для уникальности)
        user_id = hash(request.session_id) % (10**9)

        if request.mode == "admin":
            # Admin режим: используем text2sql pipeline
            logger.info(f"Admin режим: обработка вопроса от session {request.session_id[:8]}...")
            response, sql = await text2sql_manager.process_query(request.message)
            return ChatMessageResponse(response=response, mode="admin", sql_query=sql)
        else:
            # Normal режим: обычный LLM-ассистент
            logger.info(f"Normal режим: обработка сообщения от session {request.session_id[:8]}...")
            response = await normal_conversation_manager.process_message(user_id, request.message)
            return ChatMessageResponse(response=response, mode="normal")

    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}") from e


@app.post("/api/chat/clear")
async def clear_history(request: ChatClearRequest) -> dict[str, str]:
    """
    Очистить историю диалога для сессии

    Args:
        request: Запрос с session_id

    Returns:
        Статус операции

    Raises:
        HTTPException 500: При ошибке очистки истории
    """
    try:
        # Конвертируем session_id в user_id
        user_id = hash(request.session_id) % (10**9)

        # Очищаем историю для обоих режимов
        await normal_conversation_manager.clear_history(user_id)
        await admin_conversation_manager.clear_history(user_id)

        logger.info(f"История очищена для session {request.session_id[:8]}...")
        return {"status": "cleared", "session_id": request.session_id}

    except Exception as e:
        logger.error(f"Ошибка при очистке истории: {e}")
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}") from e
