import base64
import logging
import pymupdf
from pathlib import Path



from src.tools.schemas import DocSegment, LatexSeparators, VecDbRecord, ProcessedSection, DocInfo
from src.tools.segmenter import Segmenter
from src.tools.image_service import ImageProcessor
from src.tools.text_service import TextProcessor

from src.config.db import DBConfig
from src.exceptions.exceptions import  ConfigurationError

logger = logging.getLogger(__name__)

class PaperProcessor:
    def __init__(self, segmenter: Segmenter, img_proc: ImageProcessor, text_proc: TextProcessor):
        self._segmenter: Segmenter = segmenter
        self._img_proc: ImageProcessor = img_proc
        self._text_proc: TextProcessor = text_proc
        self._current_content: str = ""
        self._records: list[VecDbRecord] = []
        self._author_info: DocInfo = DocInfo(authors="", citation="", title="")
        self._arxiv_signature: str | None = None
        self._year: int | None = None

    def _verify_metadata(self):
        if self._arxiv_signature is None or self._year is None:
            raise ConfigurationError("ArXiv signature and year must be set")
        
    def _construct_file_path(self, path: str) -> Path:
        return Path(DBConfig.LOCAL_STORAGE_PATH, f"{self._arxiv_signature}_{self._year}", path)

    async def process_paper(self, path: str, arxiv_signature: str, year: int):
        self._arxiv_signature = arxiv_signature
        self._year = year

        local_path = self._construct_file_path(path)
       
        with open(local_path) as f:
            text = f.read()

        segments = self._segmenter.create_segments(text)
        async for image_event in self._prep_sections(segments):
            yield image_event
        full_sections = self._build_full_sections()

        yield{
            "event": "author_info",
            "data": self._author_info.model_dump()
        }
        
        processed: list[ProcessedSection] = []

        for i, (section_name, section_content) in enumerate(full_sections.items()):
            yield{
                "id": i,
                "event": "processed_section",
                "data": {
                    "section_name": section_name,
                    "content": section_content
                }
            }

            translated = ""
            summary = ""

            async for token in self._text_proc.translate_section(section_content):
                translated += token
                yield{
                    "id": i,
                    "event": "translated_section_token",
                    "data": {
                        "section_name": section_name,
                        "token": token
                    }
                }

            async for token in self._text_proc.summarize_section(section_content):
                summary += token
                yield{
                    "id": i,
                    "event": "summary_token",
                    "data": {
                        "section_name": section_name,
                        "token": token
                    }
                }
        
            processed.append(ProcessedSection(
                section_name=section_name,
                original_content=section_content,
                translated_content=translated,
                summary=summary
            ))
        
        yield{
            "event": "done",
            "data": {}
        }
    
    async def _process_image(self, segment: DocSegment):
        """Yield tokens for image descriptions and mutate segment.content with final text.

        Yields dicts shaped like other SSE events:
          {"event": "image_start", "data": {"filename": ..., "figure": n}}
          {"event": "image_token", "data": {"filename": ..., "token": ...}}
        """
        paths = self._segmenter.get_fig_paths(segment.content)
        descriptions: list[str] = []
        for iter, p in enumerate(paths):
            figure_label = f"Figure {iter + 1}"
            yield {
                "event": "image_start",
                "data": {"filename": p, "figure": figure_label},
            }

            description_parts: list[str] = []
            p_split = p.split('.')
            ext = p_split[-1].lower()
            local_path = self._construct_file_path(p)

            if local_path.exists():
                if ext in ["jpg", "png"]:
                    with open(local_path, "rb") as f:
                        img_b64 = base64.b64encode(f.read()).decode()
                    async for token in self._img_proc.process_stream(img_b64):
                        description_parts.append(token)
                        yield {
                            "event": "image_token",
                            "data": {"filename": p, "figure": figure_label, "token": token},
                        }
                elif ext == "pdf":
                    doc = pymupdf.open(local_path)
                    for page in doc:
                        description_parts.append(str(page.get_text())) # type: ignore
            else:
                description_parts.append("File path missing or corrupted.")
                logger.warning(f"Description omitted due to missing file at {local_path}")

            description = " ".join(part for part in description_parts if part)
            descriptions.append(f"{figure_label}: {description}")

        segment.content = " ".join(descriptions)

    async def _concatenate_segments(self, segment: DocSegment):
        if segment.type == LatexSeparators.TITLE:
            self._title = self._segmenter.get_segment_name(segment.content)

        elif segment.type == LatexSeparators.SECTION:
            if len(self._records) > 0:
                self._records[-1].content = self._current_content
                
            section = self._segmenter.get_segment_name(segment.content)
            self._current_content = " ".join([self._current_content, segment.content])

            self._records.append(VecDbRecord(section=section))
            self._current_content = ""

        elif segment.type == LatexSeparators.SUBSECTION:
            self._records[-1].content = self._current_content

            subsection = self._segmenter.get_segment_name(segment.content)
            self._current_content = " ".join([self._current_content, segment.content])

            self._records.append(VecDbRecord(section=self._records[-1].section, subsection=subsection))
            self._current_content = ""
            
        elif segment.type == LatexSeparators.TEXT or segment.type == LatexSeparators.FIGURE:
            self._current_content = " ".join([self._current_content, segment.content])

        elif segment.type == LatexSeparators.AUTHOR:
            self._author_info = await self._text_proc.infer_authors_and_citation(segment.content, 
                                                                      self._title, 
                                                                      self._arxiv_signature, # type: ignore 
                                                                      self._year) # type: ignore

    async def _prep_sections(self, segments: list[DocSegment]):
        """Async generator: builds records while yielding image-processing events."""
        for seg in segments:
            if seg.type == LatexSeparators.FIGURE:
                async for image_event in self._process_image(seg):
                    yield image_event

            await self._concatenate_segments(seg)
        if self._current_content != "":
            self._records[-1].content = self._current_content

    def _build_full_sections(self) -> dict[str, str]:
        full_sections: dict[str, str] = {}
        for r in self._records:
            full_sections[r.section] = " ".join([full_sections.get(r.section, ""), r.subsection, r.content])
        return full_sections

    
