from pydantic_settings import BaseSettings

class PostgresSettings(BaseSettings):
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

settings = PostgresSettings()
