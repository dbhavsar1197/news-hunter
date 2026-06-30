from sqlalchemy.orm import Session

from app.models.article import Article
from app.schemas.article import ArticleCreate


def create_article(db: Session, article: ArticleCreate) -> Article:
    db_article = Article(
        title=article.title,
        source=article.source,
        url=article.url,
        summary=article.summary,
        category=article.category,
        published_at=article.published_at,
    )

    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    return db_article


def get_articles(db: Session):
    return db.query(Article).all()


def get_article(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()


def delete_article(db: Session, article_id: int):
    article = get_article(db, article_id)

    if article:
        db.delete(article)
        db.commit()

    return article