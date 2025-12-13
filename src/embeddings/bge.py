from typing import List
import httpx 
from src.config import settings


class BGEEmbeddingsVLLM:
    def __init__(self):
        self.base_url=settings.EMBEDDING_BASE_URL
        self.model=settings.EMBEDDING_MODEL
        
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{self.base_url}/embeddings",
                json={"model": self.model, "input": texts},
            )
            resp.raise_for_status()
            data = resp.json()["data"]
            # OpenAI format: list of {index, embedding, object}
            data.sort(key=lambda x: x["index"])
            return [d["embedding"] for d in data]

    async def embed_query(self, query: str) -> List[float]:
        q = self._prepare_query(query)
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{self.base_url}/embeddings",
                json={"model": self.model, "input": [q]},
            )
            resp.raise_for_status()
            return resp.json()["data"][0]["embedding"]
