from sqlmodel import create_engine, Session

sqlite_file_name = "lab.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})


def get_session():
    """Dependency for getting database session."""
    with Session(engine) as session:
        yield session
