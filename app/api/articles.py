from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.article import (
    ArticleCreate,
    ArticleEnrichmentResponse,
    ArticleResponse,
)
from app.services.article_service import (
    bulk_create_articles,
    create_article,
    enrich_article,
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
    return bulk_create_articles(db, articles)


@router.post("/{article_id}/enrich", response_model=ArticleEnrichmentResponse)
def enrich(article_id: int, db: Session = Depends(get_db)):
    return enrich_article(db, article_id)
