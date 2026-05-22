from langchain.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama 

from src.config.prompts import PromptsConfig 

vl_model = ChatOllama(model="qwen3-vl:8b", temperature=0.1)

class ImageProcessor:
    def __init__(self, model: ChatOllama = vl_model):
        self._model = model 

    def process_image(self, image: str) -> str:
        res = self._model.invoke([
            SystemMessage(content=PromptsConfig.FIGURE_DESCRIPTION_SYSTEM_MESSAGE),
            HumanMessage([{
                "type": "image_url",
                "image_url": f"data:image/png;base64,{image}"
            }])
        ])

        return str(res.content)


