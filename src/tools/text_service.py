from langchain.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel

from typing import  AsyncGenerator, cast
import time

from src.tools.base import BaseLLMService 
from src.tools.schemas import DocInfo

from src.config.prompts import PromptsConfig
from src.exceptions.exceptions import LLMError




class TextProcessor(BaseLLMService):
    def __init__(self, model: BaseChatModel):
        self._model: BaseChatModel = model

    async def infer_authors_and_citation(self, authors: str, title: str, arxiv_signature: str, year: int) -> DocInfo:
        structured = self._model.with_structured_output(DocInfo)

        citation_string = f"title: {title}, authors: {authors}, arxiv signature: {arxiv_signature}, year: {year}"
        res = await self._process_structured(citation_string, PromptsConfig.AUTHOR_AND_CITATION_SYSTEM_MESSAGE, DocInfo)
        return res 

    async def translate_section(self, section: str) -> AsyncGenerator:
        async for token in self._process_stream(section, PromptsConfig.TRANSLATE_SECTION_SYSTEM_MESSAGE):
            yield token 

    async def summarize_section(self, section: str) -> AsyncGenerator:
        async for token in self._process_stream(section, PromptsConfig.SUMMARIZE_SECTION_SYSTEM_MESSAGE):
            yield token 

    