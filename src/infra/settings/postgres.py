from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    db: str
    scheme: str = "postgresql+asyncpg"

    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme=self.scheme,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db,
        )

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")
