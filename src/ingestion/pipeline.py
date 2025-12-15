# src/ingestion/pipeline.py
import uuid
from typing import List
from langchain_core.documents import Document

from src.embeddings.bge import BGEEmbeddingsVLLM   # <- vLLM embeddings client
from src.vectorstores.qdrant_store import QdrantStore  # <- your folder is vectorstores


def build_payload(doc: Document) -> dict:
    meta = doc.metadata or {}
    return {
        "text": doc.page_content,
        "doc_title": meta.get("source", "unknown"),
        "page": meta.get("page"),
        "date": meta.get("date"),
        "department": meta.get("department"),
    }


async def ingest_documents(docs: List[Document]):
    embedder = BGEEmbeddingsVLLM()
    store = QdrantStore()

    texts = [d.page_content for d in docs]
    vectors = await embedder.embed_documents(texts)  # <- async call to vLLM embeddings

    store.create_collection_if_not_exists(vector_dim=len(vectors[0]))

    payloads = [build_payload(d) for d in docs]
    ids = [str(uuid.uuid4()) for _ in docs]  # ok for now; can switch to stable IDs later

    store.upsert(ids=ids, vectors=vectors, payloads=payloads)
    print(f"Ingested {len(docs)} chunks into Qdrant.")
