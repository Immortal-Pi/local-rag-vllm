# src/retrieval/retriever.py
from typing import List, Dict, Any
from src.embeddings.bge import BGEEmbeddingsVLLM
from src.vectorstores.qdrant_store import QdrantStore
from src.reranker.bge_reranker import BGEReranker
from config import settings

class RAGRetriever:
    def __init__(self):
        self.embedder = BGEEmbeddingsVLLM()
        self.store = QdrantStore()
        self.reranker = BGEReranker()

    async def retrieve(
        self,
        query: str,
        filters: Dict[str, Any] | None = None,
        k_candidates: int = 100,
        k_final: int = 8,
    ) -> List[Dict[str, Any]]:
        query_vec = await self.embedder.embed_query(query)
        results = self.store.hybrid_search(
            query_vector=query_vec, limit=k_candidates, filters=filters
        )

        passages = [
            {"id": r.id, "score": r.score, **(r.payload or {})}
            for r in results
            if r.payload and "text" in r.payload
        ]

        reranked = self.reranker.rerank(
            query=query,
            passages=passages,
            top_k=k_final,
            text_key="text",
        )
        return reranked
