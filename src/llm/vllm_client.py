# src/llm/vllm_client.py
from typing import List, Dict
import httpx
from src.config import settings
import requests

class VLLMClient:
    def __init__(self):
        self.base_url = settings.LLM_BASE_URL
        self.model = settings.LLM_MODEL_NAME

    # async def chat(
    #     self,
    #     messages: List[Dict[str, str]],
    #     temperature: float = 0.2,
    #     max_tokens: int = 512,
    # ) -> str:
    #     async with httpx.AsyncClient(timeout=90.0) as client:
    #         resp = await client.post(
    #             f"{self.base_url}/chat/completions",
    #             json={
    #                 "model": self.model,
    #                 "messages": messages,
    #                 "temperature": temperature,
    #                 "max_tokens": max_tokens,
    #             },
    #         )
    #         resp.raise_for_status()
    #         data = resp.json()
    #         return data["choices"][0]["message"]["content"]
    def chat(self, system_prompt: str, user_prompt: str):
        payload = {
            "model": settings.LLM_MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.1,
            "max_tokens": 1300,
        }

        resp = requests.post(
            f"{settings.LLM_BASE_URL}/chat/completions",
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
