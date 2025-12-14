import asyncio
from src.retrieval.retriever import RAGRetriever

async def main():
    r = RAGRetriever()
    out = await r.retrieve(
        query="What did Tesla report as revenue in 2023?",
        filters={"department": "finance"},
        k_candidates=20,
        k_final=5,
    )

    print("\nReranked results:")
    for i, p in enumerate(out, 1):
        print(f"{i}. rerank_score={p.get('rerank_score'):.4f} doc={p.get('doc_title')}")
        print(p["text"][:200], "...\n")

if __name__ == "__main__":
    asyncio.run(main())
