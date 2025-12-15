import asyncio
from src.rag.pipeline import RAGPipeline

async def main():
    rag = RAGPipeline()
    out = await rag.ask(
        query="What is physical resource layer? give a detailed answer",
        filters=None,
        k=5,
    )

    print("\nANSWER:\n", out["answer"])
    print("\nSOURCES:")
    for s in out["sources"]:
        print(s)

if __name__ == "__main__":
    asyncio.run(main())
