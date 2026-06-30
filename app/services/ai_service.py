from __future__ import annotations

import os
import re
from typing import Optional


class AIService:
    """Small wrapper around LLM-based article summarization and categorization."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini") -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def summarize_article(self, title: str, content: str, max_length: int = 180) -> str:
        """Return a concise summary for a news article."""
        if not title and not content:
            return ""

        prompt = (
            "Summarize the following article in 2-3 sentences. "
            "Keep the wording concise and factual.\n\n"
            f"Title: {title}\n\nContent: {content}"
        )

        summary = self._call_llm(prompt)
        if summary:
            return self._trim_to_length(summary, max_length)

        return self._fallback_summary(title, content, max_length)

    def classify_article(self, title: str, content: str) -> str:
        """Return a simple category label for an article."""
        prompt = (
            "Classify the article into one short category label. "
            "Use a simple label such as AI, Business, Tech, Politics, Health, or World.\n\n"
            f"Title: {title}\n\nContent: {content}"
        )

        category = self._call_llm(prompt)
        if category:
            return self._normalize_category(category)

        return self._fallback_category(title, content)

    def _call_llm(self, prompt: str) -> str:
        if not self.api_key:
            return ""

        try:
            from openai import OpenAI
        except ImportError:
            return ""

        try:
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            return (response.choices[0].message.content or "").strip()
        except Exception:
            return ""

    def _fallback_summary(self, title: str, content: str, max_length: int) -> str:
        if title and content:
            base = f"{title}. {content[:220]}"
        elif title:
            base = title
        else:
            base = content[:220]

        return self._trim_to_length(base, max_length)

    def _fallback_category(self, title: str, content: str) -> str:
        text = f"{title} {content}".lower()

        if any(word in text for word in ["ai", "gpt", "llm", "model", "openai", "agent"]):
            return "AI"
        if any(word in text for word in ["finance", "business", "market", "company", "startup"]):
            return "Business"
        if any(word in text for word in ["health", "medical", "hospital", "drug"]):
            return "Health"
        if any(word in text for word in ["election", "government", "policy", "politics"]):
            return "Politics"

        return "Tech"

    def _normalize_category(self, category: str) -> str:
        cleaned = re.sub(r"[^a-zA-Z\s]", "", category).strip()
        if not cleaned:
            return "Tech"
        return cleaned.split()[0].capitalize()

    def _trim_to_length(self, text: str, max_length: int) -> str:
        if len(text) <= max_length:
            return text
        return text[: max_length - 3].rstrip() + "..."
