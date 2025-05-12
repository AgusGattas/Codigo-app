from sqlalchemy import func, select
from typing import List, Dict

from app.core.config import settings
from app.dependency_registry import registry
from app.modules.asistencias.models import Asistencia
from app.repositories.sql_repository import SQLAlchemyRepository


class AsistenciaRepository:
    """Base repository interface for Asistencia"""


class AsistenciaSQLRepository(SQLAlchemyRepository[Asistencia]):
    model: Asistencia = Asistencia

    def get_by_partido(self, partido_id: int) -> List[Asistencia]:
        """Get all asistencias for a specific partido
        Args:
            partido_id (int): The ID of the partido
        Returns:
            List[Asistencia]: List of asistencias for the partido
        """
        return self.get_all(base_query=select(self.model).where(self.model.partido_id == partido_id))

    def get_by_jugador(self, jugador_id: int) -> List[Asistencia]:
        """Get all asistencias for a specific jugador
        Args:
            jugador_id (int): The ID of the jugador
        Returns:
            List[Asistencia]: List of asistencias for the jugador
        """
        return self.get_all(base_query=select(self.model).where(self.model.jugador_id == jugador_id))

    def get_resumen_jugadores(self) -> List[Dict]:
        """Get a summary of asistencias by jugador
        Returns:
            List[Dict]: List of dictionaries with jugador_id, total_partidos, and total_presentes
        """
        return self.db_session.execute(
            select(
                self.model.jugador_id,
                func.count(self.model.id).label('total_partidos'),
                func.sum(func.case((self.model.presente == True, 1), else_=0)).label('total_presentes')
            ).group_by(self.model.jugador_id)
        ).all()


repositories = {
    "SQL": AsistenciaSQLRepository,
}

registry.register(
    AsistenciaRepository,
    to=repositories[settings.REPOSITORY_NAME],
) 