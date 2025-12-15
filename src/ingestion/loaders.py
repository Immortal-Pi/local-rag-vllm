from __future__ import annotations

from typing import List
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


SUPPORTED_TEXT_EXTS = {".txt", ".md"}
SUPPORTED_PDF_EXTS = {".pdf"}


def load_docs_from_folder(folder: str) -> List[Document]:
    """
    Load PDFs and text files from a folder recursively.

    Produces LangChain Document objects with metadata including:
      - source: file path
      - file_name
      - file_ext
      - (for PDFs) page
    """
    folder_path = Path(folder).expanduser().resolve()
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    docs: List[Document] = []

    for path in folder_path.rglob("*"):
        if not path.is_file():
            continue

        ext = path.suffix.lower()
        if ext in SUPPORTED_PDF_EXTS:
            loader = PyPDFLoader(str(path))
            loaded = loader.load()
            # enrich metadata
            for d in loaded:
                d.metadata = d.metadata or {}
                d.metadata["source"] = str(path)
                d.metadata["file_name"] = path.name
                d.metadata["file_ext"] = ext
            docs.extend(loaded)

        elif ext in SUPPORTED_TEXT_EXTS:
            loader = TextLoader(str(path), encoding="utf-8")
            loaded = loader.load()
            for d in loaded:
                d.metadata = d.metadata or {}
                d.metadata["source"] = str(path)
                d.metadata["file_name"] = path.name
                d.metadata["file_ext"] = ext
            docs.extend(loaded)

    return docs
