from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./futbol_app.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def recreate_tables():
    """
    Recrea todas las tablas de la base de datos.
    ¡ADVERTENCIA! Esto eliminará todos los datos existentes.
    """
    from .models import models
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

def recreate_core_tables():
    """
    Recrea solo las tablas principales (jugadores, partidos, estadísticas).
    ¡ADVERTENCIA! Esto eliminará todos los datos existentes.
    """
    from .models import models
    # Eliminar todas las tablas
    models.Base.metadata.drop_all(bind=engine)
    
    # Crear solo las tablas principales
    models.Jugador.__table__.create(engine)
    models.Partido.__table__.create(engine)
    models.Estadistica.__table__.create(engine)
    models.Asistencia.__table__.create(engine) 