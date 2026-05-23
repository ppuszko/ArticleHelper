from langchain.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
import time

from config.prompts import PromptsConfig 


class ImageProcessor:
    def __init__(self, model: BaseChatModel):
        self._model: BaseChatModel = model 

    def process_image(self, image: str) -> str:
        start = time.time()
        
        res = self._model.invoke([
            SystemMessage(content=PromptsConfig.FIGURE_DESCRIPTION_SYSTEM_MESSAGE),
            HumanMessage([{
                "type": "image_url",
                "image_url": f"data:image/png;base64,{image}"
            }])
        ])
        end = time.time()
        print(f"Img proc time: {(end - start):.2f}")

        return str(res.content)


