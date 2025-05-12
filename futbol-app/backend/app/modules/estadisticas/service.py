"""Module with the service related to the estadisticas service"""

from typing import List, Type
from uuid import UUID

from fastapi_pagination import Params
from injector import inject
from sqlalchemy import select

from app.core.base.service import BaseService
from app.modules.estadisticas.models import Estadistica
from app.modules.estadisticas.repository import EstadisticaRepository
from app.modules.estadisticas.schemas import EstadisticaCreate, EstadisticaUpdate


class EstadisticaService(BaseService[Estadistica, EstadisticaCreate, EstadisticaUpdate]):
    @inject
    def __init__(self, repository: EstadisticaRepository):
        super().__init__(repository)

    def get_by_jugador(self, jugador_id: UUID) -> List[Estadistica]:
        """Get all statistics for a specific player."""
        return self.repository.get_by_jugador(jugador_id)

    def get_by_partido(self, partido_id: UUID) -> List[Estadistica]:
        """Get all statistics for a specific match."""
        return self.repository.get_by_partido(partido_id)

    def create_bulk(self, estadisticas: List[EstadisticaCreate]) -> List[Estadistica]:
        """Create multiple statistics."""
        return self.repository.create_bulk(estadisticas)

    def delete_by_jugador(self, jugador_id: UUID) -> None:
        """Delete all statistics for a specific player."""
        self.repository.delete_by_jugador(jugador_id)

    def delete_by_partido(self, partido_id: UUID) -> None:
        """Delete all statistics for a specific match."""
        self.repository.delete_by_partido(partido_id) 