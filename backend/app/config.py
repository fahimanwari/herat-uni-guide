from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    jwt_secret: str
    ai_provider: str = "gemini"
    ai_model: str = "gemini-2.5-flash"
    ai_api_key: str = ""
    storage_provider: str = "local"
    allowed_origins: str = "http://localhost:4000,https://guide.hu.edu.af"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
