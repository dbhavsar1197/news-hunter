from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ArticleCreate(BaseModel):
    title: str
    source: str
    url: str
    summary: str | None = None
    category: str | None = None
    published_at: datetime | None = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    source: str
    url: str
    summary: str | None = None
    category: str | None = None
    published_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)