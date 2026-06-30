from __future__ import annotations

import json
import os
import re
from typing import Any, Optional


class AIService:
    """Wrapper around article enrichment with a safe fallback path."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"

    def enrich_article(self, article: Any) -> dict[str, Any]:
        title = getattr(article, "title", "") or ""
        source = getattr(article, "source", "") or ""
        summary = getattr(article, "summary", "") or ""
        category = getattr(article, "category", "") or ""
        url = getattr(article, "url", "") or ""

        prompt = (
            "You are enriching a news article for a backend system.\n"
            "Return ONLY valid JSON with these keys:\n"
            'summary: a concise 2-3 sentence summary,\n'
            'category: one short category label,\n'
            "keywords: an array of 3-8 short keyword strings,\n"
            'sentiment: one of "positive", "neutral", or "negative",\n'
            "importance: a number from 1 to 10.\n\n"
            f"Title: {title}\n"
            f"Source: {source}\n"
            f"Existing summary: {summary}\n"
            f"Existing category: {category}\n"
            f"URL: {url}"
        )

        payload = self._call_llm(prompt)
        if payload:
            parsed = self._parse_enrichment_payload(payload)
            if parsed:
                return parsed

        return self._fallback_enrichment(title, source, summary, category, url)

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
                response_format={"type": "json_object"},
            )
            return (response.choices[0].message.content or "").strip()
        except Exception:
            return ""

    def _parse_enrichment_payload(self, payload: str) -> dict[str, Any]:
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", payload, re.DOTALL)
            if not match:
                return {}

            try:
                data = json.loads(match.group(0))
            except json.JSONDecodeError:
                return {}

        summary = str(data.get("summary", "")).strip()
        category = self._normalize_category(str(data.get("category", "")))
        keywords = self._normalize_keywords(data.get("keywords"))
        sentiment = self._normalize_sentiment(str(data.get("sentiment", "")))
        importance = self._normalize_importance(data.get("importance"))

        if not summary:
            return {}

        return {
            "ai_summary": summary,
            "ai_category": category,
            "keywords": keywords,
            "sentiment": sentiment,
            "importance_score": importance,
        }

    def _fallback_enrichment(
        self,
        title: str,
        source: str,
        summary: str,
        category: str,
        url: str,
    ) -> dict[str, Any]:
        base_text = " ".join(part for part in [title, summary, source, url] if part).strip()
        text = base_text.lower()

        fallback_summary = summary or title or source or url
        if summary and title and summary != title:
            fallback_summary = f"{title}. {summary}"
        fallback_summary = self._trim_to_length(fallback_summary, 220)

        fallback_category = category or self._fallback_category(title, summary or source)
        fallback_keywords = self._fallback_keywords(text or fallback_summary.lower())
        fallback_sentiment = self._fallback_sentiment(text or fallback_summary.lower())
        fallback_importance = self._fallback_importance(text or fallback_summary.lower())

        return {
            "ai_summary": fallback_summary,
            "ai_category": fallback_category,
            "keywords": fallback_keywords,
            "sentiment": fallback_sentiment,
            "importance_score": fallback_importance,
        }

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

    def _fallback_keywords(self, text: str) -> list[str]:
        keywords = []
        for term in ["ai", "openai", "llm", "model", "agent", "business", "health", "politics", "technology"]:
            if term in text and term not in keywords:
                keywords.append(term)

        return keywords[:8] or ["news"]

    def _fallback_sentiment(self, text: str) -> str:
        positive_terms = ["growth", "gain", "improve", "launch", "win", "expand"]
        negative_terms = ["risk", "decline", "concern", "loss", "slowdown", "breach"]

        if any(term in text for term in positive_terms):
            return "positive"
        if any(term in text for term in negative_terms):
            return "negative"

        return "neutral"

    def _fallback_importance(self, text: str) -> float:
        score = 5.0
        if any(term in text for term in ["openai", "gpt", "llm", "ai", "model"]):
            score += 2.0
        if any(term in text for term in ["launch", "partnership", "report", "research", "funding"]):
            score += 1.0
        if any(term in text for term in ["security", "safety", "enterprise", "inference"]):
            score += 1.0

        return min(score, 10.0)

    def _normalize_category(self, category: str) -> str:
        cleaned = re.sub(r"[^a-zA-Z\s]", "", category).strip()
        if not cleaned:
            return "Tech"
        return cleaned.split()[0].capitalize()

    def _normalize_keywords(self, keywords: Any) -> list[str]:
        if not isinstance(keywords, list):
            return []

        normalized: list[str] = []
        for keyword in keywords:
            text = str(keyword).strip()
            if text and text not in normalized:
                normalized.append(text)

        return normalized[:8]

    def _normalize_sentiment(self, sentiment: str) -> str:
        cleaned = sentiment.strip().lower()
        if cleaned in {"positive", "neutral", "negative"}:
            return cleaned
        return "neutral"

    def _normalize_importance(self, importance: Any) -> float:
        try:
            value = float(importance)
        except (TypeError, ValueError):
            return 5.0

        return max(1.0, min(value, 10.0))

    def _trim_to_length(self, text: str, max_length: int) -> str:
        if len(text) <= max_length:
            return text
        return text[: max_length - 3].rstrip() + "..."
