from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Intelligent Content API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "changethis"  # In prod, use a strong secret from env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db" # Default to SQLite for local dev

    class Config:
        env_file = ".env"

settings = Settings()
