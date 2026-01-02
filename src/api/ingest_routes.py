from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import asyncio

from src.ingestion.upload_loader import load_uploaded_file
from src.ingestion.chunking import chunk_documents
from src.ingestion.pipeline import ingest_documents

router = APIRouter(prefix="/ingest", tags=["ingestion"])

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_and_ingest(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    ext = Path(file.filename).suffix.lower()
    if ext not in {".pdf", ".txt", ".md"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Save file temporarily
    temp_path = UPLOAD_DIR / file.filename
    with temp_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        docs = load_uploaded_file(temp_path)
        chunks = chunk_documents(docs)

        # For now: single-user system
        await ingest_documents(chunks)

        return {
            "status": "success",
            "filename": file.filename,
            "chunks_indexed": len(chunks),
        }

    finally:
        # Optional: delete file after ingestion
        if temp_path.exists():
            temp_path.unlink()
