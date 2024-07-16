from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    """
    Crea la base de datos y las tablas si no existen.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Genera una sesión de base de datos para realizar operaciones en la base de datos.
    """
    with Session(engine) as session:
        yield session
