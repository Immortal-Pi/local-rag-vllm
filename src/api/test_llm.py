import requests
import json

LLM_URL = "http://172.202.46.95:8000/v1/chat/completions"
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

payload = {
    "model": MODEL_NAME,
    "messages": [
        {"role": "system", "content": "You are a helpful assistant generation."},
        {"role": "user", "content": "Explain RAG in LLM in one sentence."}
    ],
}

response = requests.post(
    LLM_URL,
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload),
    timeout=30
)

response.raise_for_status()
result = response.json()

print("LLM response:")
print(result["choices"][0]["message"]["content"])
