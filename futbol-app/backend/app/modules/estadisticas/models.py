from __future__ import annotations
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.database.mixins import TimestampMixin

class Estadistica(TimestampMixin, Base):
    __tablename__ = "estadisticas"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    jugador_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jugadores.id", ondelete="CASCADE"))
    partido_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("partidos.id", ondelete="CASCADE"))
    goles: Mapped[int] = mapped_column(default=0)
    asistencias: Mapped[int] = mapped_column(default=0)
    tarjetas_amarillas: Mapped[int] = mapped_column(default=0)
    tarjetas_rojas: Mapped[int] = mapped_column(default=0)
    minutos_jugados: Mapped[int] = mapped_column(default=0)
    titular: Mapped[bool] = mapped_column(default=False)

    # Relaciones
    jugador: Mapped["Jugador"] = relationship("Jugador", backref="estadisticas", lazy="joined")
    partido: Mapped["Partido"] = relationship("Partido", backref="estadisticas", lazy="joined") 