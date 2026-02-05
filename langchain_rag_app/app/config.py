import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = "sk-..." # Default or from env
    CHROMA_DB_DIR: str = "chroma_db"
    MODEL_NAME: str = "gpt-3.5-turbo"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"

settings = Settings()
