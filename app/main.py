from fastapi import FastAPI

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
