from langchain.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel

from typing import cast
import time

from tools.schemas import AuthorsInfo, SectionInfo
from config.prompts import PromptsConfig


tex_model = ChatGoogleGenerativeAI(model="gpt-oss-safeguard:20b", temperature=0, num_ctx=8192)

class TextProcessor:
    def __init__(self, model: BaseChatModel = tex_model):
        self._model: BaseChatModel = model

    def infer_authors(self, authors: str, title: str) -> AuthorsInfo:
        temp = self._model.with_structured_output(AuthorsInfo)

        start = time.time()
        res = temp.invoke([
            SystemMessage(
                PromptsConfig.AUTHOR_AND_CITATION_SYSTEM_MESSAGE
            ),
            HumanMessage([
                {
                    "type": "text",
                    "text": f"title: {title}, authors: {authors}"
                }
            ]
        )])
        end = time.time()
        print(f"Author proc time: {(end - start):.2f}")

        return cast(AuthorsInfo, res) 

    def process_section(self, section: str) -> SectionInfo:
        temp = self._model.with_structured_output(SectionInfo)
        print(len(section))
        
        for attempt in range(2):
            try:
                start = time.time()
                res = temp.invoke([
                    SystemMessage(
                        PromptsConfig.SECTION_SYSTEM_MESSAGE
                    ),
                    HumanMessage([
                        {
                            "type": "text",
                            "text": section
                        }, 
                    ])
                ])
                end = time.time()
                print(f"Section proc time: {(end - start):.2f}")

                return cast(SectionInfo, res)
            except Exception:
                print(f"Attemp {attempt} failed. Retrying")
                time.sleep(1)
        print("ALl attempts failed. Defaulting to empty SectionInfo")
        return SectionInfo(translated_content="", summary="")
        
    