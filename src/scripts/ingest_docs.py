# scripts/ingest_docs.py
import asyncio
from src.ingestion.loaders import load_docs_from_folder
from src.ingestion.chunking import chunk_documents
from src.ingestion.pipeline import ingest_documents

def main():
    folder = "data/raw_docs"
    docs = load_docs_from_folder(folder)
    chunks = chunk_documents(docs)
    asyncio.run(ingest_documents(chunks))

if __name__ == "__main__":
    main()
