from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="News Hunter API",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "application": "News Hunter",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
