from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List, ForwardRef
from enum import Enum

class TipoEvento(str, Enum):
    ENTRENAMIENTO = "ENTRENAMIENTO"
    PARTIDO = "PARTIDO"

# Definir referencias adelantadas
EstadisticaRef = ForwardRef('Estadistica')
PartidoRef = ForwardRef('Partido')

class JugadorBase(BaseModel):
    nombre: str
    activo: bool = True

class JugadorCreate(JugadorBase):
    pass

class Jugador(JugadorBase):
    id: int

    class Config:
        from_attributes = True

class AsistenciaBase(BaseModel):
    fecha: date
    tipo: TipoEvento
    presente: bool = True

class AsistenciaCreate(AsistenciaBase):
    jugador_id: int

class Asistencia(AsistenciaBase):
    id: int
    jugador_id: int

    class Config:
        from_attributes = True

class PartidoBase(BaseModel):
    fecha: date
    rival: str
    resultado_local: Optional[int] = None
    resultado_visitante: Optional[int] = None
    lugar: str
    tipo: str

class PartidoCreate(PartidoBase):
    pass

class Partido(PartidoBase):
    id: int

    class Config:
        from_attributes = True

class EstadisticaBase(BaseModel):
    jugador_id: int
    partido_id: int
    goles: int = 0
    asistencias: int = 0
    tarjetas_amarillas: int = 0
    tarjetas_rojas: int = 0
    minutos_jugados: int = 0
    titular: bool = False

class EstadisticaCreate(EstadisticaBase):
    pass

class Estadistica(EstadisticaBase):
    id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True

class EstadisticasJugador(BaseModel):
    jugador_id: int
    nombre_jugador: str
    total_partidos: int
    total_goles: int
    total_asistencias: int
    total_amarillas: int
    total_rojas: int
    minutos_totales: int
    promedio_minutos: float

class EstadisticasPartido(BaseModel):
    partido_id: int
    fecha: datetime
    rival: str
    local: bool
    goles_favor: int
    goles_contra: int
    jugadores: List[Estadistica]

# Actualizar las referencias adelantadas
Partido.update_forward_refs()
Estadistica.update_forward_refs() 