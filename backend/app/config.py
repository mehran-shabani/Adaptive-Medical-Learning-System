"""
Application configuration management.
Loads settings from environment variables.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "Adaptive Medical Learning System"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql://medical_user:medical_password@localhost:5432/adaptive_medical_learning"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT Authentication
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # OpenAI API
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000

    # Vector Database
    USE_PGVECTOR: bool = True
    QDRANT_URL: str | None = None
    QDRANT_API_KEY: str | None = None
    VECTOR_DIMENSION: int = 1536  # text-embedding-3-small dimension

    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 50
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_EXTENSIONS: list = [".pdf"]

    # Content Processing
    CHUNK_SIZE_MIN: int = 300  # minimum words per chunk
    CHUNK_SIZE_MAX: int = 700  # maximum words per chunk
    CHUNK_OVERLAP: int = 50  # word overlap between chunks

    # Quiz Settings
    DEFAULT_QUIZ_SIZE: int = 5
    QUIZ_TIME_LIMIT_SECONDS: int = 300  # 5 minutes per quiz

    # Mastery Algorithm
    MASTERY_INITIAL_SCORE: float = 0.0
    MASTERY_CORRECT_INCREMENT: float = 0.1
    MASTERY_INCORRECT_DECREMENT: float = 0.05
    MASTERY_WEAK_THRESHOLD: float = 0.7  # Below this is considered weak

    # Recommender Settings
    STUDY_PLAN_DURATION_MINUTES: int = 120  # 2 hours
    SPACED_REPETITION_THRESHOLD_DAYS: int = 2

    # OTP Settings (Mock for development)
    OTP_LENGTH: int = 6
    OTP_EXPIRY_MINUTES: int = 5
    OTP_PROVIDER: str = "mock"  # Options: mock, kavenegar
    KAVENEGAR_API_KEY: str | None = None
    KAVENEGAR_OTP_TEMPLATE: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
