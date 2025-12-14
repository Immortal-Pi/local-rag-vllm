import requests
import json

EMBED_URL = "http://172.202.46.95:8001/v1/embeddings"
MODEL_NAME = "BAAI/bge-large-en-v1.5"

payload = {
    "model": MODEL_NAME,
    "input": "Retrieval augmented generation improves factual accuracy."
}

response = requests.post(
    EMBED_URL,
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload),
    timeout=30
)

response.raise_for_status()
result = response.json()

embedding = result["data"][0]["embedding"]

print(f"Embedding length: {len(embedding)}")
print("First 10 values:", embedding[:10])
