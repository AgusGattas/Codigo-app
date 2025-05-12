from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import and_

from app.modules.estadisticas.models import Estadistica

class EstadisticaFilters(BaseModel):
    jugador_id: Optional[int] = None
    partido_id: Optional[int] = None
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None
    goles_min: Optional[int] = None
    goles_max: Optional[int] = None
    asistencias_min: Optional[int] = None
    asistencias_max: Optional[int] = None
    tarjetas_amarillas_min: Optional[int] = None
    tarjetas_amarillas_max: Optional[int] = None
    tarjetas_rojas_min: Optional[int] = None
    tarjetas_rojas_max: Optional[int] = None
    minutos_jugados_min: Optional[int] = None
    minutos_jugados_max: Optional[int] = None
    titular: Optional[bool] = None 

class EstadisticaFilter(Filter):
    jugador_id: UUID | None = None
    partido_id: UUID | None = None
    fecha_desde: datetime | None = None
    fecha_hasta: datetime | None = None
    goles_min: int | None = None
    goles_max: int | None = None
    asistencias_min: int | None = None
    asistencias_max: int | None = None

    class Config:
        model = Estadistica

    def apply(self, query):
        if self.jugador_id:
            query = query.filter(Estadistica.jugador_id == self.jugador_id)
        if self.partido_id:
            query = query.filter(Estadistica.partido_id == self.partido_id)
        if self.goles_min is not None:
            query = query.filter(Estadistica.goles >= self.goles_min)
        if self.goles_max is not None:
            query = query.filter(Estadistica.goles <= self.goles_max)
        if self.asistencias_min is not None:
            query = query.filter(Estadistica.asistencias >= self.asistencias_min)
        if self.asistencias_max is not None:
            query = query.filter(Estadistica.asistencias <= self.asistencias_max)
        return query 