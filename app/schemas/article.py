from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ArticleCreate(BaseModel):
    title: str
    source: str
    url: str
    summary: str | None = None
    category: str | None = None
    published_at: datetime | None = None
    ai_summary: str | None = None
    ai_category: str | None = None
    keywords: list[str] | None = None
    sentiment: str | None = None
    importance_score: float | None = None
    processed_at: datetime | None = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    source: str
    url: str
    summary: str | None = None
    category: str | None = None
    published_at: datetime | None = None
    created_at: datetime
    ai_summary: str | None = None
    ai_category: str | None = None
    keywords: list[str] | None = None
    sentiment: str | None = None
    importance_score: float | None = None
    processed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ArticleEnrichmentResponse(BaseModel):
    ai_summary: str | None = None
    ai_category: str | None = None
    keywords: list[str] = Field(default_factory=list)
    sentiment: str | None = None
    importance_score: float | None = None
    processed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
