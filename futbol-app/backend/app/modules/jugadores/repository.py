from sqlalchemy import delete, select
from typing import List, Optional

from app.core.config import settings
from app.dependency_registry import registry
from app.modules.jugadores.models import Jugador
from app.repositories.sql_repository import SQLAlchemyRepository


class JugadorRepository:
    """Base repository interface for Jugador"""


class JugadorSQLRepository(SQLAlchemyRepository[Jugador]):
    model: Jugador = Jugador

    def get_by_numero(self, numero: int) -> Optional[Jugador]:
        """Get a jugador by its number
        Args:
            numero (int): The number of the jugador
        Returns:
            Optional[Jugador]: The jugador if found, None otherwise
        """
        return self.get_all(base_query=select(self.model).where(self.model.numero == numero))

    def get_activos(self) -> List[Jugador]:
        """Get all active jugadores
        Returns:
            List[Jugador]: List of active jugadores
        """
        return self.get_all(base_query=select(self.model).where(self.model.activo == True))


repositories = {
    "SQL": JugadorSQLRepository,
}

registry.register(
    JugadorRepository,
    to=repositories[settings.REPOSITORY_NAME],
) 