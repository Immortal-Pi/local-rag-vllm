# src/embeddings/bge.py
from typing import List
import httpx
import math
from src.config import settings

def _l2_normalize(vec: List[float]) -> List[float]:
    norm = math.sqrt(sum(x*x for x in vec)) or 1.0
    return [x / norm for x in vec]

class BGEEmbeddingsVLLM:
    def __init__(self):
        self.base_url = settings.EMBEDDING_BASE_URL
        self.model = settings.EMBEDDING_MODEL
        self.query_instruction = settings.QUERY_INSTRUCTION

    def _prep_query(self, query: str) -> str:
        return self.query_instruction + query

    async def _embed(self, inputs: List[str]) -> List[List[float]]:
        async with httpx.AsyncClient(timeout=180.0) as client:
            resp = await client.post(
                f"{self.base_url}/embeddings",
                json={"model": self.model, "input": inputs},
            )
            resp.raise_for_status()
            data = resp.json()["data"]
            data.sort(key=lambda x: x["index"])
            vectors = [d["embedding"] for d in data]
            # if settings.NORMALIZE_EMBEDDINGS:
            #     vectors = [_l2_normalize(v) for v in vectors]
            return vectors

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return await self._embed(texts)

    async def embed_query(self, query: str) -> List[float]:
        return (await self._embed([self._prep_query(query)]))[0]
