from sqlmodel import create_engine, Session
import os

# Database configuration - supports SQLite (dev) and PostgreSQL (prod)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///lab.db")

# Create engine with appropriate settings based on database type
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration for development
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration for production
    # Uses connection pooling for better performance
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Test connections before using
        pool_recycle=3600     # Recycle connections every hour
    )


def get_session():
    """Dependency for getting database session."""
    with Session(engine) as session:
        yield session
