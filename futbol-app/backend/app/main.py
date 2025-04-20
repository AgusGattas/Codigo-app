from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import jugadores, partidos, estadisticas
from .database import engine
from .models import models

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fútbol App API", description="API para gestionar elementos del equipo de fútbol")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(jugadores.router, tags=["jugadores"])
app.include_router(partidos.router, tags=["partidos"])
app.include_router(estadisticas.router, tags=["estadisticas"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Fútbol App"} 