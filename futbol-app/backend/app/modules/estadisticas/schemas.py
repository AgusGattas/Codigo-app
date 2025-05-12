from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from typing import Optional

class EstadisticaBase(BaseModel):
    jugador_id: UUID
    partido_id: UUID
    goles: int = 0
    asistencias: int = 0
    tarjetas_amarillas: int = 0
    tarjetas_rojas: int = 0
    minutos_jugados: int = 0
    titular: bool = False

class EstadisticaCreate(EstadisticaBase):
    pass

class EstadisticaUpdate(BaseModel):
    goles: int | None = None
    asistencias: int | None = None
    tarjetas_amarillas: int | None = None
    tarjetas_rojas: int | None = None
    minutos_jugados: int | None = None
    titular: bool | None = None

class EstadisticaResponse(EstadisticaBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EstadisticaJugador(BaseModel):
    jugador_id: UUID
    nombre: str
    apellido: str
    goles: int = 0
    asistencias: int = 0
    tarjetas_amarillas: int = 0
    tarjetas_rojas: int = 0
    minutos_jugados: int = 0
    titular: bool = False

    class Config:
        from_attributes = True 