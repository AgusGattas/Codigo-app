from app.database import recreate_tables

if __name__ == "__main__":
    print("Recreando tablas de la base de datos...")
    recreate_tables()
    print("¡Migración completada!") 