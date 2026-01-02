# src/rag/pipeline.py
from src.retrieval.retriever import RAGRetriever
from src.llm.vllm_client import VLLMClient
from src.config import settings

SYSTEM_PROMPT = """You are a helpful assistant.
When answering:
- Provide a detailed, structured explanation
- Use multiple paragraphs
- Give concrete examples from the context
- Explain performance, limitations, and implications
- Do NOT give one-line answers

If the question asks for examples, provide multiple examples.
If the question asks about performance, include qualitative and quantitative observations.

Base your answer strictly on the provided context.
"""

class RAGPipeline:
    def __init__(self):
        self.retriever = RAGRetriever()
        self.llm = VLLMClient()

    def _build_context(self, passages, max_chars=12000):
        chunks = []
        total = 0
        for p in passages:
            text = p["text"].strip()
            if total + len(text) > max_chars:
                break
            chunks.append(text)
            total += len(text)
        return "\n\n---\n\n".join(chunks)

    async def ask(self, query: str, filters=None, k=5):
        passages = await self.retriever.retrieve(
            query=query,
            filters=filters,
            k_final=k,
        )

        context = self._build_context(passages)

        prompt = f"""
Context:
{context}

Question:
{query}

Answer:
"""

        answer = self.llm.chat(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
        )

        return {
            "answer": answer,
            "sources": [
                {
                    "doc_title": p.get("doc_title"),
                    "page": p.get("page"),
                }
                for p in passages
            ],
        }
