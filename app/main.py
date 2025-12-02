from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import auth, content
from app.db.base import Base
from app.db.session import engine

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(content.router, prefix=f"{settings.API_V1_STR}/contents", tags=["contents"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Intelligent Content API"}
