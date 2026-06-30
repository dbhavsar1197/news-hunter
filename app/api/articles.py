from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.article import ArticleCreate, ArticleResponse
from app.services.article_service import create_article, get_articles

router = APIRouter(
    prefix="/articles",
    tags=["Articles"]
)


@router.post("/", response_model=ArticleResponse)
def create(article: ArticleCreate, db: Session = Depends(get_db)):
    return create_article(db, article)


@router.get("/", response_model=list[ArticleResponse])
def read_all(db: Session = Depends(get_db)):
    return get_articles(db)