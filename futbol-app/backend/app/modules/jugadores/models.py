from __future__ import annotations
from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from sqlalchemy import  String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.database.mixins import TimestampMixin

class Jugador(TimestampMixin, Base):
    __tablename__ = "jugadores"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    nombre: Mapped[str] = mapped_column(String(100))
    apellido: Mapped[str] = mapped_column(String(100))
    mail: Mapped[str] = mapped_column(String(100))
    fecha_ficha_medica: Mapped[datetime] = mapped_column()
    fecha_nacimiento: Mapped[datetime] = mapped_column()
    posicion: Mapped[str] = mapped_column(String(50))
    numero: Mapped[int] = mapped_column(unique=True)
    activo: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    asistencias: Mapped[List["Asistencia"]] = relationship("Asistencia", back_populates="jugador", lazy="joined", cascade="all, delete-orphan") 