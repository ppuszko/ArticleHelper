from fastapi import Request

from src.tools.paper_processor import PaperProcessor
from src.tools.text_service import TextProcessor
from src.tools.image_service import ImageProcessor
from src.tools.segmenter import Segmenter
from src.tools.file_manager import FileManager

from src.exceptions.exceptions import ServiceMissingError

def get_paper_processor(request: Request) -> PaperProcessor:
    try:
        img_model = getattr(request.app.state, "img_proc_model")
        img_proc = ImageProcessor(img_model)
    except AttributeError as e:
        raise ServiceMissingError(f"Image processor model missing: {str(e)}")  
    
    try:
        text_proc_model = getattr(request.app.state, "text_proc_model")
        text_proc = TextProcessor(text_proc_model)
    except AttributeError as e:
        raise ServiceMissingError(f"Text processor model not found: {str(e)}")  
    
    segmenter = Segmenter() 

    return PaperProcessor(segmenter, img_proc, text_proc)


def get_file_processor() -> FileManager:
    return FileManager()