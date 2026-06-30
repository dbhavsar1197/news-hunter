from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleResponse
from app.services.article_service import (
    create_article,
    get_articles
)

router = APIRouter(prefix="/articles", tags=["Articles"])


# single insert
@router.post("/", response_model=ArticleResponse)
def create(article: ArticleCreate, db: Session = Depends(get_db)):
    return create_article(db, article)


# get all
@router.get("/", response_model=list[ArticleResponse])
def read_all(db: Session = Depends(get_db)):
    return get_articles(db)


# bulk insert (CLEAN VERSION)
@router.post("/bulk")
def create_bulk(
    articles: List[ArticleCreate],
    db: Session = Depends(get_db)
):
    inserted = 0
    skipped = 0
    results = []

    for article in articles:
        existing = db.query(Article).filter(Article.url == article.url).first()

        if existing:
            skipped += 1
            results.append(existing)
            continue

        db_article = create_article(db, article)

        inserted += 1
        results.append(db_article)

    return {
        "inserted": inserted,
        "skipped": skipped,
        "total": len(articles),
        "data": results
    }