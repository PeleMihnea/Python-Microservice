# src/math_microservice/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Math Microservice"
    VERSION: str = "0.1.0"
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# a single, importable settings instance
settings = Settings()

# DEBUG: make sure .env is loading the container URL
print("▶ FastAPI will connect to:", settings.DATABASE_URL)
