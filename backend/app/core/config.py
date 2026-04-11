from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):
    """
    Application settings using Pydantic BaseSettings.
    Loads environment variables from .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    KAFKA_BROKER_URL: str = "localhost:9092"
    KAFKA_TOPIC_SUPPORT_TICKETS: str = "support.tickets.new"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Constructs the async database URL from individual components.
        Uses the asyncpg driver.
        """
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )


settings = Settings()
