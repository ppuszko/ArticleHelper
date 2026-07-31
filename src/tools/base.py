import asyncio
import logging
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel
from typing import Callable, TypeVar, Type, cast
from functools import wraps
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from src.config.ai import AIConfig

logger = logging.getLogger(__name__)

def guard_llm_call(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = None
        last_exception = None

        # First, attempt the call once to see what kind of callable it is
        try:
            result = await func(*args, **kwargs)
        except (asyncio.TimeoutError, Exception) as e:
            last_exception = e
            logger.warning(f"LLM call failed on first attempt: {e}")
            # If first call fails, retry with backoff
            for attempt in range(1, AIConfig.RETRIES + 1):
                try:
                    await asyncio.sleep([20, 40, 60][min(attempt - 1, 2)])
                    logger.info(f"Retrying LLM call (attempt {attempt}/{AIConfig.RETRIES})...")
                    result = await func(*args, **kwargs)
                    break
                except (asyncio.TimeoutError, Exception) as e2:
                    last_exception = e2
                    logger.warning(f"LLM call failed on retry attempt {attempt}: {e2}")
            else:
                logger.error(f"LLM call failed after {AIConfig.RETRIES} retries. Last error: {last_exception}")
                raise last_exception
        return result

    return wrapper

T = TypeVar("T", bound=BaseModel)

class BaseLLMService(ABC):
    def __init__(self, model: BaseChatModel):
        self._model = model

    @guard_llm_call
    async def _process(self, content: str | list[str | dict], system_message: str) -> AIMessage:
        res = await self._model.ainvoke([
            SystemMessage(content=system_message),
            HumanMessage(content=content)
        ])
        return res
    

    async def _process_stream(self, content: str | list[str | dict], system_message: str) -> AsyncGenerator[AIMessage, None]:
        last_exception = None
        
        try:
            stream = self._model.astream([
                SystemMessage(system_message),
                HumanMessage(content=content)
            ])
            async for chunk in stream:
                yield chunk
        except (Exception) as e:
            last_exception = e
            logger.warning(f"LLM call failed on first attempt: {e}")
            # If first call fails, retry with backoff
            for attempt in range(1, AIConfig.RETRIES + 1):
                try:
                    await asyncio.sleep([20, 40, 60][min(attempt - 1, 2)])
                    logger.info(f"Retrying LLM call (attempt {attempt}/{AIConfig.RETRIES})...")
                    break
                except (Exception) as e2:
                    last_exception = e2
                    logger.warning(f"LLM call failed on retry attempt {attempt}: {e2}")
                    raise

    @guard_llm_call
    async def _process_structured(self, content: str | list[str | dict], system_message: str, schema: Type[T]) -> T:
        structured = self._model.with_structured_output(schema)
        res = await structured.ainvoke([
            SystemMessage(content=system_message),
            HumanMessage(content=content) 
        ])
        return cast(T, res)

    def _stringify(self, message: AIMessage) -> str:
        """Extract the text content from an AI message, skipping non-text parts.

        When a model returns structured or mixed content (e.g. from structured
        output or tool-call metadata), we only surface the actual textual answer.
        """
        if isinstance(message.content, str):
            return message.content
        if isinstance(message.content, list):
            return " ".join(
                str(part)
                for part in message.content
                if isinstance(part, str) and part.strip()
            )
        return str(message.content)
        
    