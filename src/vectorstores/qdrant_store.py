from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from config import settings


class QdrantStore:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )
        self.collection = settings.QDRANT_COLLECTION

    # ---------------------------------------------------------
    # Collection management
    # ---------------------------------------------------------
    def create_collection_if_not_exists(self, vector_dim: int):
        collections = self.client.get_collections().collections
        existing = {c.name for c in collections}

        if self.collection not in existing:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=vector_dim,
                    distance=Distance.COSINE,
                ),
            )

    # ---------------------------------------------------------
    # Upsert points
    # ---------------------------------------------------------
    def upsert(
        self,
        ids: List[str],
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
    ):
        assert len(ids) == len(vectors) == len(payloads)

        points = [
            PointStruct(
                id=pid,
                vector=vec,
                payload=payload,
            )
            for pid, vec, payload in zip(ids, vectors, payloads)
        ]

        self.client.upsert(
            collection_name=self.collection,
            points=points,
        )

    # ---------------------------------------------------------
    # Vector / hybrid search
    # ---------------------------------------------------------
    def hybrid_search(
        self,
        query_vector: List[float],
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
    ):
        qdrant_filter = None

        if filters:
            conditions = [
                FieldCondition(
                    key=key,
                    match=MatchValue(value=value),
                )
                for key, value in filters.items()
            ]
            qdrant_filter = Filter(must=conditions)

        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=limit,
            query_filter=qdrant_filter,
            with_payload=True,
        )

        return results
