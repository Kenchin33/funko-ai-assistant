from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Funko AI Assistant API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "funko_ai_assistant"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"

    OPENROUTER_API_KEY: str | None = None
    OPENROUTER_MODEL: str = "openrouter/free"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()