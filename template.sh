#!/bin/bash

# creating directory structure
mkdir -p src
mkdir -p src/embeddings
mkdir -p src/vectorstores
mkdir -p src/reranker
mkdir -p src/ingestion
mkdir -p src/retrieval
mkdir -p src/llm
mkdir -p src/rag
mkdir -p src/api
mkdir -p research
mkdir -p static/assets

# creating files 
touch src/__init__.py
touch src/helper.py 
touch src/prompt.py
touch src/embeddings/bge.py
touch src/vectorstores/qdrant_store.py
touch src/reranker/bge_reranker.py
touch src/ingestion/loaders.py
touch src/ingestion/chunking.py 
touch src/ingestion/pipeline.py 
touch src/retrieval/retriever.py 
touch src/llm/vllm_client.py 
touch src/rag/pipeline.py
touch src/api/server.py 
touch config.py
touch .env 
touch setup.py 
touch app.py 
touch research/trails.ipynb 
touch requirements.txt 

echo "Directory and files created successfully"
