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
    section: str    

class DocSegment(BaseModel):
    type: LatexSeparators
    content: str = ""

class AuthorsInfo(BaseModel):
    """Author list and ciation"""
    authors: str = Field("Comma-separated list of authors.")
    citation: str = Field("Citation formula for given resource.")