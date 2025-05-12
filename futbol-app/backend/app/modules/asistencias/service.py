from typing import List, Dict
from uuid import UUID

from injector import Inject

from app.modules.asistencias.repository import AsistenciaRepository
from app.modules.asistencias.schemas import AsistenciaCreate, AsistenciaUpdate
from app.services.base_crud_service import BaseService
from app.modules.asistencias.models import Asistencia


class AsistenciaService(BaseService):
    def __init__(self, repo: Inject[AsistenciaRepository]):
        super().__init__(repo)

    def get_by_partido(self, partido_id: int) -> List[Asistencia]:
        return self.repo.get_by_partido(partido_id)

    def get_by_jugador(self, jugador_id: int) -> List[Asistencia]:
        return self.repo.get_by_jugador(jugador_id)

    def get_resumen_jugadores(self) -> List[Dict]:
        return self.repo.get_resumen_jugadores() 