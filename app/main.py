from fastapi import FastAPI

from app.db.database import engine
from app.db.base import Base
from app.api.articles import router as article_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="News Hunter API",
    version="1.0.0"
)

app.include_router(article_router)


@app.get("/")
async def root():
    return {"application": "News Hunter", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}