from pydantic import BaseModel, Field 

from uuid import UUID 
from enum import StrEnum

class LatexSeparators(StrEnum):
    TITLE = "\\title{"
    AUTHOR = "\\author{"
    SECTION = "\\section{"
    SUBSECTION = "\\subsection{"
    FIGURE = "\\begin{figure}"
    ABSTRACT = "\\begin{abstract}"
    COMMENT = "%"
    TEXT = "\n"

class VecDbRecord(BaseModel):
    section: str
    subsection: str = ""
    content: str = ""
    doc_id: UUID | None = None 

class SectionInfo(BaseModel):
    """Translated and cleaned section content and section summary"""
    translated_content: str
    summary: str 

class ProcessedSection(SectionInfo):
    section_name: str    
    original_content: str

class DocSegment(BaseModel):
    type: LatexSeparators
    content: str = ""

class DocInfo(BaseModel):
    """Title, author list and ciation for scientific paper"""
    authors: str = Field("Comma-separated list of authors.")
    citation: str = Field("Citation formula for given resource.")
    title: str = Field("Title of the paper")