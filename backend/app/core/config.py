from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Darukaa.Earth API"

    # Runtime connection: uses port 6543 (transaction pooler) on Supabase for application traffic
    DATABASE_URL: str = "postgresql://postgres:password@localhost:6543/postgres"

    # Migration connection: uses port 5432 (direct) because DDL migrations require session mode
    DATABASE_URL_DIRECT: str = "postgresql://postgres:password@localhost:5432/postgres"

    # JWT Authentication configuration
    JWT_SECRET_KEY: str = "darukaa-super-secret-jwt-key-for-local-dev-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    # Default 24-hour token expiration for session convenience during active development
    JWT_EXPIRE_MINUTES: int = 1440

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
