from pydantic import BaseModel, Field


class ProcessDirectoryRequest(BaseModel):
    directory: str = Field(..., description="Path to the directory containing .tex file")
    arxiv_signature: str = Field(..., description="ArXiv signature")
    year: int = Field(..., description="Year of publication")