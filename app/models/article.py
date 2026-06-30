from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.sql import func

from app.db.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    source = Column(String(255), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)
    summary = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    ai_summary = Column(Text, nullable=True)
    ai_category = Column(String(100), nullable=True)
    keywords = Column(JSON, nullable=True)
    sentiment = Column(String(50), nullable=True)
    importance_score = Column(Float, nullable=True)
    processed_at = Column(DateTime, nullable=True)
