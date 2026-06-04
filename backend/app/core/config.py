from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://nutrition:nutrition@localhost:5432/nutrition_ai"
    ai_provider: str = "mock"

    gemini_api_key: str
    gemini_embedding_model: str = "gemini-embedding-001"
    embedding_dimension: int = 3072
    retrieval_similarity_threshold: float = 0.70

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
