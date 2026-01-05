import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from src.api.ingest_routes import router as ingest_router
from src.config import settings 
from src.logging.audit import ensure_log_table, log_rag_to_db, get_client_ip

# Your RAG pipeline
from src.rag.pipeline import RAGPipeline


# ----------------------------
# App
# ----------------------------
app = FastAPI(title="RAG Chat API")
app.include_router(ingest_router)
# If you will open index.html via file:// or via a different port, keep CORS.
# If you serve /ui from FastAPI and set API="/ask", you can tighten/remove CORS later.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8080",
        "http://localhost:8080",
        # "http://127.0.0.1:8000",
        # "http://localhost:8000",
        "null",
        "*",  # dev-friendly; tighten in prod
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Startup
# ----------------------------
@app.on_event("startup")
def on_startup() -> None:
    app.state.rag = RAGPipeline()
    # Load UI once
    try:
        app.state.html_page = Path("index.html").read_text(encoding="utf-8")
        ensure_log_table(settings.PG_URI, settings.PG_SCHEMA)
    except FileNotFoundError:
        app.state.html_page = "<h1>index.html not found</h1>"


# ----------------------------
# Schemas
# ----------------------------
class AskRequest(BaseModel):
    question: str
    # keep for compatibility with your frontend checkbox
    want_viz: Optional[bool] = True

    # optional filter support (you can pass {"department":"finance"} later)
    filters: Optional[Dict[str, Any]] = None
    k: int = 5


class SourceItem(BaseModel):
    doc_title: Optional[str] = None
    page: Optional[int] = None


class AskResponse(BaseModel):
    # RAG response fields
    answer: Optional[str] = None
    sources: List[SourceItem] = Field(default_factory=list)

    # Keep these keys so your existing renderer doesn’t break (optional)
    sql_string: Optional[str] = None
    columns: List[str] = Field(default_factory=list)
    rows: List[Dict[str, Any]] = Field(default_factory=list)
    plotly_figure: Optional[Dict[str, Any]] = None
    vega_spec: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# ----------------------------
# Routes
# ----------------------------
@app.get("/ping")
def ping():
    return {"ok": True}


@app.get("/ui", response_class=HTMLResponse)
def ui():
    return app.state.html_page


@app.post("/ask", response_model=AskResponse)
async def ask_endpoint(req: AskRequest, request: Request):
    rag: RAGPipeline = getattr(app.state, "rag", None)
    if rag is None:
        raise HTTPException(status_code=500, detail="RAG pipeline not initialized")

    q = (req.question or "").strip()
    if not q:
        return AskResponse(error="Empty question")

    client_ip=get_client_ip(request)
    # user_id=None
    try:
        out = await rag.ask(
            query=q,
            filters=req.filters,  # can be None
            k=req.k,
        )

        log_rag_to_db(
            pg_uri=settings.PG_URI,
            schema=settings.PG_SCHEMA,
            client_ip=client_ip,
            question=q,
            response=out.get("answer"),
            sources=out.get("sources"),
            error=None,
        )

        # out expected like: {"answer": "...", "sources": [{"doc_title":..., "page":...}, ...]}
        return AskResponse(
            answer=out.get("answer"),
            sources=[SourceItem(**s) for s in (out.get("sources") or [])],
            error=None,
        )

    except Exception as e:
        
        log_rag_to_db(
            pg_uri=settings.PG_URI,
            schema=settings.PG_SCHEMA,
            client_ip=client_ip,
            question=q,
            response=None,
            sources=None,
            error=str(e),
        )
        return AskResponse(error=str(e))


# ----------------------------
# Dev entrypoint
# ----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.server:app", host="127.0.0.1", port=8080, reload=False, workers=1)
