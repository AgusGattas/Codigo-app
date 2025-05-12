from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class AsistenciaBase(BaseModel):
    jugador_id: int
    partido_id: int
    presente: bool
    justificacion: Optional[str] = None

class AsistenciaCreate(AsistenciaBase):
    pass

class AsistenciaUpdate(BaseModel):
    presente: Optional[bool] = None
    justificacion: Optional[str] = None

class AsistenciaResponse(AsistenciaBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AsistenciaJugador(BaseModel):
    jugador_id: int
    total_partidos: int
    total_presentes: int

    class Config:
        from_attributes = True 