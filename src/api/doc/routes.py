import json
from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.sse import EventSourceResponse, ServerSentEvent

from src.api.dependencies import get_paper_processor, get_file_processor, PaperProcessor, FileManager
from src.exceptions.exceptions import BadRequest

doc_router = APIRouter()


@doc_router.post("/process-directory")
async def process_directory(
    file: UploadFile = File(...),
    arxiv_signature: str = Form(...),
    year: int = Form(...),
    file_processor: FileManager = Depends(get_file_processor)
):
    if not file.filename or not file.filename.endswith(".gz"):
        raise BadRequest("Uploaded file must be a .gz archive")
    if file_processor.check_paper_exist(arxiv_signature, year):
        raise BadRequest("Paper already exists")
    saved = await file_processor.process_directory(file.file, arxiv_signature, year)

    return saved


@doc_router.get("/process-paper", response_class=EventSourceResponse)
async def process_paper(
    tex_file: str,
    arxiv_signature: str,
    year: int,
    paper_processor: PaperProcessor = Depends(get_paper_processor)
):
    async for event in paper_processor.process_paper(tex_file, arxiv_signature, year):
        # Pass the dict directly; ServerSentEvent will handle the JSON serialization.
        payload = {"event": event.get("event"), "data": event.get("data", {})}
        yield ServerSentEvent(data=payload)



