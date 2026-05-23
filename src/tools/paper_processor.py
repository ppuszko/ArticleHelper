
import base64
import pymupdf

from .schemas import DocSegment, LatexSeparators, VecDbRecord, ProcessedSection
from .segmenter import Segmenter
from .image_processor import ImageProcessor
from .text_processor import TextProcessor

from ollama import Client

oc = Client()

class PaperProcessor:
    def __init__(self, segmenter: Segmenter, img_proc: ImageProcessor, text_proc: TextProcessor):
        self._segmenter: Segmenter = segmenter
        self._img_proc: ImageProcessor = img_proc
        self._text_proc: TextProcessor = text_proc
        self._current_content: str = ""
        self._records: list[VecDbRecord] = []
        self._full_sections = {}
        self._author: str = ""
    
    def process_image(self, segment: DocSegment):
        paths = self._segmenter.get_fig_paths(segment.content)
        content = "Figure(s) description:"
        for p in paths:
            temp = ""
            print(p)
            p_split = p.split('.')

            if p_split[-1] in ["jpg", "png"]:
                with open(f"files/{p}", "rb") as f:
                    file = f.read()
                img_b64 = base64.b64encode(file).decode()
                temp = self._img_proc.process_image(img_b64)
            elif p_split[-1] == "pdf":
                doc = pymupdf.open(f"files/{p}")
                for page in doc:
                    temp = " ".join([temp, str(page.get_text())]) # type: ignore
            else:
                temp = p
            content = " ".join([content, temp])
        segment.content = content

    def concatenate_segments(self, segment: DocSegment):
        if segment.type == LatexSeparators.TITLE:
            self._title = self._segmenter.get_marker_name(segment.content)
        elif segment.type == LatexSeparators.SECTION:
            if len(self._records) > 0:
                self._records[-1].content = self._current_content
                
            section = self._segmenter.get_marker_name(segment.content)
            self._current_content = " ".join([self._current_content, segment.content])

            self._records.append(VecDbRecord(section=section))
            self._current_content = ""
        elif segment.type == LatexSeparators.SUBSECTION:
            self._records[-1].content = self._current_content

            subsection = self._segmenter.get_marker_name(segment.content)
            self._current_content = " ".join([self._current_content, segment.content])

            self._records.append(VecDbRecord(section=self._records[-1].section, subsection=subsection))
            self._current_content = ""
        elif segment.type == LatexSeparators.TEXT or segment.type == LatexSeparators.FIGURE:
            self._current_content = " ".join([self._current_content, segment.content])
        elif segment.type == LatexSeparators.AUTHOR:
            self._author = segment.content

    def prep_sections(self, segments: list[DocSegment]):
        for seg in segments:
            if seg.type == LatexSeparators.FIGURE:
                self.process_image(seg)
            self.concatenate_segments(seg)
        if self._current_content != "":
            self._records[-1].content = self._current_content

        for r in self._records:
            self._full_sections[r.section] = " ".join([self._full_sections.get(r.section, ""), r.content])


        oc.generate(model="qwen3-vl:8b", keep_alive=0)


    def process_paper(self, path: str) -> list[ProcessedSection]:
        with open(path) as f:
            text = f.read()

        segments = self._segmenter.create_segments(text)
        self.prep_sections(segments)
        
        processed = []
        for k, v in self._full_sections.items():
            section = self._text_proc.process_section(v)
            processed.append(ProcessedSection(**(section.model_dump()), section=k))

        return processed
