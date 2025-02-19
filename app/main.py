from fastapi import FastAPI
from app.routes import scoring, health
from app.config import settings

app = FastAPI(title="Scoring API", version="1.0.0")

# Include Routes
app.include_router(scoring.router, prefix="/scoring", tags=["Scoring"])
app.include_router(health.router, prefix="/health", tags=["Health"])

@app.get("/")
def home():
    return {"message": "Welcome to the Scoring API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
