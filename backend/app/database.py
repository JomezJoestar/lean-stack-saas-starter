import os
from collections.abc import Generator
from sqlmodel import create_engine, SQLModel, Session

# We'll use a local SQLite file named 'dev.db'
sqlite_file_name = "dev.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args={"check_same_thread": False} is required specifically for SQLite 
# to allow FastAPI's asynchronous multi-threaded requests to access it safely.
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def init_db() -> None:
    """Creates the database tables based on our SQLModel metadata."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session per request 
    and automatically closes it when the request is finished.
    """
    with Session(engine) as session:
        yield session