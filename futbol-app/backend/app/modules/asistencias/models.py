from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.database.mixins import TimestampMixin

class Asistencia(TimestampMixin, Base):
    __tablename__ = "asistencias"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    jugador_id: Mapped[int] = mapped_column(ForeignKey("jugadores.id"))
    partido_id: Mapped[int] = mapped_column(ForeignKey("partidos.id"))
    presente: Mapped[bool] = mapped_column(default=True)
    justificacion: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    jugador: Mapped["Jugador"] = relationship("Jugador", back_populates="asistencias")
    partido: Mapped["Partido"] = relationship("Partido", back_populates="asistencias") 