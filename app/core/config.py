from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Настройки для базы данных
    # DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"

    # # Development
    # DEBUG_MODE: bool = False

    # # Telegram
    # TG_BOT_TOKEN: str = ""
    # TG_SUPPORT_CHAT_ID: int | None = None

    # # MAX
    # MAX_BOT_TOKEN: str = ""
    # MAX_SUPPORT_CHAT_ID: int | None = None

    # # JWT
    # SECRET_KEY: str = "your-secret-key"
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # # REFRESH_TOKEN_EXPIRE_DAYS: int = 1

    # PostgreSQL
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "test_user"
    POSTGRES_PASSWORD: str = "test_password"
    POSTGRES_DB: str = "test_db"

    # # Redis
    # REDIS_HOST: str = "localhost"
    # REDIS_PORT: int = 6379

    # # MinIO
    # S3_HOST_URL: str = "http://localhost:9000"
    # S3_ACCESS_KEY: str = "minioadmin"
    # S3_SECRET_KEY: str = "minioadmin"
    # S3_BUCKET: str = "events"
    # S3_MATERIALS_PUBLIC_URL: str = "https://novorossiisk.app/img"

    # # Image settings
    # IMAGE_MAX_SIZE_MB: int = 10

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
