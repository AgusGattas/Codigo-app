from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class JugadorBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    fecha_ficha_medica: datetime
    fecha_nacimiento: datetime
    posicion: str
    numero: int
    activo: bool = True


class JugadorCreate(JugadorBase):
    pass


class JugadorUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    posicion: Optional[str] = None
    numero: Optional[int] = None
    activo: Optional[bool] = None


class JugadorResponse(JugadorBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 