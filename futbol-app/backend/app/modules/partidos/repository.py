from sqlalchemy import delete, select
from typing import List, Optional
from datetime import datetime

from app.core.config import settings
from app.dependency_registry import registry
from app.modules.partidos.models import Partido
from app.repositories.sql_repository import SQLAlchemyRepository


class PartidoRepository:
    """Base repository interface for Partido"""


class PartidoSQLRepository(SQLAlchemyRepository[Partido]):
    model: Partido = Partido

    def get_by_fecha(self, fecha: datetime) -> List[Partido]:
        """Get all partidos for a specific date
        Args:
            fecha (datetime): The date to filter by
        Returns:
            List[Partido]: List of partidos for the date
        """
        return self.get_all(base_query=select(self.model).where(self.model.fecha == fecha))

    def get_by_tipo(self, tipo: str) -> List[Partido]:
        """Get all partidos of a specific type
        Args:
            tipo (str): The type of partido to filter by
        Returns:
            List[Partido]: List of partidos of the specified type
        """
        return self.get_all(base_query=select(self.model).where(self.model.tipo == tipo))


repositories = {
    "SQL": PartidoSQLRepository,
}

registry.register(
    PartidoRepository,
    to=repositories[settings.REPOSITORY_NAME],
) 