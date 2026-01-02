from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

def load_uploaded_file(path: Path) -> list[Document]:
    ext = path.suffix.lower()

    if ext == ".pdf":
        loader = PyPDFLoader(str(path))
        docs = loader.load()
    elif ext in {".txt", ".md"}:
        loader = TextLoader(str(path), encoding="utf-8")
        docs = loader.load()
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # normalize metadata
    for d in docs:
        d.metadata = d.metadata or {}
        d.metadata["source"] = path.name

    return docs
