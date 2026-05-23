from langchain.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama 

import time

from config.prompts import PromptsConfig 

vl_model = ChatOllama(model="qwen3-vl:8b", temperature=0.1)



class ImageProcessor:
    def __init__(self, model: ChatOllama = vl_model):
        self._model = model 

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


