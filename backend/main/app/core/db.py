from pydantic_core import MultiHostUrl
from sqlmodel import SQLModel, Session, create_engine, select
from app.core.config import settings

DATABASE_URL = str(MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT,
            path=settings.POSTGRES_DB,
        ))
engine = create_engine(DATABASE_URL)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    
def reset_db() -> None:
    """Drop all tables and recreate them fresh."""
    print("Dropping all tables...")
    SQLModel.metadata.drop_all(engine)
    print("Creating all tables...")
    SQLModel.metadata.create_all(engine)
    print("Database reset complete!")
