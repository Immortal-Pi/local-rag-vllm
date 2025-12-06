# creating directory
mkdir -p src 
mkdir -p research 
mkdir -p static/assets

# creating files 
touch src/__init__.py
touch src/helper.py 
touch src/prompt.py
touch src/embeddings/bge.py
touch src/vectorstores/qdrant_store.py
touch src/reranker/bge_reranker.py 

torch src/ingestion/loaders.py
torch src/ingestion/chunking.py 
torch src/ingestion/pipeline.py 

torch src/retrieval/retriever.py 
torch src/llm/vllm_client.py 
torch src/rag/pipeline.py
torch src/api/server.py 

touch config.py
touch .env 
touch setup.py 
touch app.py 
touch research/trails.ipynb 
touch requirements.txt 

echo "Directory and files created successfully" 