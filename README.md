# 🧠 Local RAG System with vLLM & Qdrant

A **local, production-ready Retrieval-Augmented Generation (RAG) system** built using **FastAPI**, **vLLM**, **Qdrant**, and **BGE embeddings**.  
This project is designed for **low-latency inference**, **scalable document ingestion**, and **modular experimentation** with GenAI systems.

---

## System Architecture 

![arc](https://github.com/Immortal-Pi/local-rag-vllm/blob/main/static/assets/rag.png)

## 🚀 Features

- ⚡ Low-latency LLM inference using **vLLM**
- 🔍 Vector search powered by **Qdrant**
- 🧩 Modular RAG pipeline (ingestion, retrieval, reranking, generation)
- 📄 Document ingestion via API and CLI
- 🌐 FastAPI backend
- 💬 Lightweight chat UI
- 🔐 Environment-based configuration using `.env`

---

## 📐 High-Level Architecture

```
Documents
   ↓
Loaders → Chunking → Embeddings
   ↓
Qdrant Vector Store
   ↓
Retriever → (Optional Reranker)
   ↓
vLLM (LLM Inference)
   ↓
FastAPI Response
```

---

## 📁 Project Structure

```
local-rag-vllm/
│
├── src/
│   ├── api/
│   │   ├── ingest_routes.py
│   │   ├── server.py
│   │   └── test_llm.py
│   │
│   ├── embeddings/
│   │   ├── bge.py
│   │   └── test_embedding.py
│   │
│   ├── ingestion/
│   │   ├── loaders.py
│   │   ├── upload_loader.py
│   │   ├── chunking.py
│   │   └── pipeline.py
│   │
│   ├── llm/
│   │   └── vllm_client.py
│   │
│   ├── rag/
│   │   └── pipeline.py
│   │
│   ├── reranker/
│   │   └── bge_reranker.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── scripts/
│   │   ├── ingest_docs.py
│   │   ├── test_rag_pipeline.py
│   │   └── test_retriever.py
│   │
│   ├── vectorstores/
│   │   ├── qdrant_store.py
│   │   ├── test_qdrant_basic.py
│   │   └── qdrant_test.ipynb
│   │
│   └── config.py
│
├── static/
│   ├── assets/
│   │   └── rag.png
│   └── chat.html
│
├── storage/
├── .env
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── README.md
└── template.sh
```



## 📄 License

MIT (or organization-specific license)
