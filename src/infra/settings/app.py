from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    port: int = 8000
    host: str = "0.0.0.0"
    reload: bool = False
