from src.tools.base import BaseLLMService
import time
import logging 
from src.config.prompts import PromptsConfig 

logger = logging.getLogger(__name__)

class ImageProcessor(BaseLLMService): 
    async def process(self, image: str) -> str:
        start = time.time()
        
        res = await self._process(
            [{
                "type": "image_url",
                "image_url": f"data:image/png;base64,{image}"
            }], 
            PromptsConfig.FIGURE_DESCRIPTION_SYSTEM_MESSAGE)    
        
        end = time.time()
        logger.info(f"Image proc time: {(end - start):.2f}")

        return self._stringify(res)
 
    async def process_stream(self, image: str):
        stream = self._process_stream(
            [{
                "type": "image_url",
                "image_url": f"data:image/png;base64,{image}"
            }],
            PromptsConfig.FIGURE_DESCRIPTION_SYSTEM_MESSAGE)

        async for chunk in stream:
            token = self._stringify(chunk)
            if token:
                yield token


