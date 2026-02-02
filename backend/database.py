from sqlmodel import create_engine

sqlite_file_name = "lab.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})
