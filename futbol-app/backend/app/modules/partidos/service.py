from typing import List
from uuid import UUID
from datetime import datetime

from injector import Inject

from app.modules.partidos.models import Partido
from app.modules.partidos.repository import PartidoRepository
from app.modules.partidos.schemas import PartidoCreate, PartidoUpdate
from app.services.base_crud_service import BaseService


class PartidoService(BaseService):
    def __init__(self, repo: Inject[PartidoRepository]):
        super().__init__(repo)

    def get_by_fecha(self, fecha: datetime) -> List[Partido]:
        return self.repo.get_by_fecha(fecha)

    def get_by_tipo(self, tipo: str) -> List[Partido]:
        return self.repo.get_by_tipo(tipo) 