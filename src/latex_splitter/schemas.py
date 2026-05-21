from pydantic import BaseModel 

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
    subsection: str 
    content: str 
    doc_id: UUID | None = None 

class DocSegment(BaseModel):
    type: LatexSeparators
    content: str = ""
