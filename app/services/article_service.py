from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.article import Article
from app.schemas.article import ArticleCreate
from app.services.ai_service import AIService


def create_article(db: Session, article: ArticleCreate) -> Article:
    db_article = Article(
        title=article.title,
        source=article.source,
        url=article.url,
        summary=article.summary,
        category=article.category,
        published_at=article.published_at,
        ai_summary=article.ai_summary,
        ai_category=article.ai_category,
        keywords=article.keywords,
        sentiment=article.sentiment,
        importance_score=article.importance_score,
        processed_at=article.processed_at,
    )

    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    return db_article


def get_articles(db: Session):
    return db.query(Article).all()


def bulk_create_articles(db: Session, articles: list[ArticleCreate]):
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
        "data": results,
    }


def enrich_article(db: Session, article_id: int):
    article = get_article(db, article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    ai_service = AIService()
    ai_result = ai_service.enrich_article(article)

    article.ai_summary = ai_result.get("ai_summary")
    article.ai_category = ai_result.get("ai_category")
    article.keywords = ai_result.get("keywords")
    article.sentiment = ai_result.get("sentiment")
    article.importance_score = ai_result.get("importance_score")
    article.processed_at = datetime.utcnow()

    db.add(article)
    db.commit()
    db.refresh(article)

    return ai_result


def get_article(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()


def delete_article(db: Session, article_id: int):
    article = get_article(db, article_id)

    if article:
        db.delete(article)
        db.commit()

    return article
