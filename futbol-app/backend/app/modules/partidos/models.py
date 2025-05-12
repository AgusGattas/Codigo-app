from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin


class Partido(TimestampMixin, Base):
    __tablename__ = "partidos"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    fecha: Mapped[datetime] = mapped_column()
    rival: Mapped[str] = mapped_column(String(100))
    resultado_local: Mapped[int] = mapped_column()
    resultado_visitante: Mapped[int] = mapped_column()
    lugar: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[str] = mapped_column(String(50))

    # Relaciones
    asistencias: Mapped[List["Asistencia"]] = relationship(back_populates="partido", cascade="all, delete-orphan")
    estadisticas: Mapped[List["Estadistica"]] = relationship(back_populates="partido", cascade="all, delete-orphan") 