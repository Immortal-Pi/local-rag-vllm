from __future__ import annotations

from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def chunk_documents(
    docs: List[Document],
    chunk_size: int = 450,
    chunk_overlap: int = 150,
) -> List[Document]:
    """
    Chunk documents into overlapping text chunks.

    Notes:
    - Finance docs often benefit from slightly larger chunks.
    - Keeps metadata from the original documents (source, page, etc.).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(docs)
