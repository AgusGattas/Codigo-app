from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

from uuid import UUID

class TipoPartido(str, Enum):
    PARTIDO = "PARTIDO"
    ENTRENAMIENTO = "ENTRENAMIENTO"
    AMISTOSO = "AMISTOSO"

class PartidoBase(BaseModel):
    fecha: datetime
    rival: str
    resultado_local: int
    resultado_visitante: int
    lugar: str
    tipo: str

class PartidoCreate(PartidoBase):
    pass

class PartidoUpdate(BaseModel):
    fecha: Optional[datetime] = None
    rival: Optional[str] = None
    resultado_local: Optional[int] = None
    resultado_visitante: Optional[int] = None
    lugar: Optional[str] = None
    tipo: Optional[str] = None

class PartidoResponse(PartidoBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Partido(PartidoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# class PartidoWithStats(Partido):
#     estadisticas: List[Estadistica] = []
#     asistencias: List[Asistencia] = []

#     class Config:
#         from_attributes = True 