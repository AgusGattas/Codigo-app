import os
import sys
from app.database import recreate_core_tables

if __name__ == "__main__":
    print("Limpiando la base de datos...")
    recreate_core_tables()
    print("Base de datos limpiada exitosamente. Se han eliminado todas las tablas excepto jugadores, partidos, estadísticas y asistencias.") 