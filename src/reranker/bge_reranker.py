from typing import List, Dict, Any
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from src.config import settings


class BGEReranker:
    def __init__(self, device: str | None = None):
        self.tokenizer = AutoTokenizer.from_pretrained(settings.RERANKER_MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            settings.RERANKER_MODEL_NAME
        )
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    def rerank(
        self,
        query: str,
        passages: List[Dict[str, Any]],
        top_k: int = 10,
        text_key: str = "text",
    ) -> List[Dict[str, Any]]:
        if not passages:
            return []

        pairs = [[query, p.get(text_key, "")] for p in passages]

        enc = self.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=512,
        )
        enc = {k: v.to(self.device) for k, v in enc.items()}

        with torch.inference_mode():
            logits = self.model(**enc).logits  # shape: [B, 1] or [B, 2]

            if logits.dim() == 2 and logits.size(-1) == 1:
                scores = logits.squeeze(-1)
            elif logits.dim() == 2 and logits.size(-1) >= 2:
                # common convention: index 1 = "relevant"
                scores = logits[:, 1]
            else:
                scores = logits.view(-1)

            scores = scores.detach().float().cpu().tolist()

        scored = [{**p, "rerank_score": float(s)} for p, s in zip(passages, scores)]
        scored.sort(key=lambda x: x["rerank_score"], reverse=True)
        return scored[:top_k]
