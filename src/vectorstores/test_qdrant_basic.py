import asyncio
import uuid 
from src.vectorstores.qdrant_store import QdrantStore
from src.embeddings.bge import BGEEmbeddingsVLLM

async def main():
    store = QdrantStore()
    embed = BGEEmbeddingsVLLM()

    texts = [
        "Tesla 2023 revenue was reported in the 10-K filing.",
        "Apple sells iPhones and services worldwide.",
        "Interest rates impact bank net interest margins."
    ]

    vecs = await embed.embed_documents(texts)
    store.create_collection_if_not_exists(vector_dim=len(vecs[0]))

    ids = [str(uuid.uuid4()) for _ in texts]
    payloads = [
        {"text": texts[0], "doc_title": "tesla_10k", "department": "finance"},
        {"text": texts[1], "doc_title": "apple_overview", "department": "product"},
        {"text": texts[2], "doc_title": "bank_note", "department": "finance"},
    ]

    store.upsert(ids=ids, vectors=vecs, payloads=payloads)

    q = "Tesla revenue in 2023"
    qvec = await embed.embed_query(q)

    results = store.hybrid_search(query_vector=qvec, limit=5, filters={"department": "finance"})

    print("\nTop matches:")
    for r in results:
        print("ID:", r.id, "score:", r.score, "title:", r.payload.get("doc_title"))
        print("text:", r.payload.get("text")[:120], "...\n")

if __name__ == "__main__":
    asyncio.run(main())
