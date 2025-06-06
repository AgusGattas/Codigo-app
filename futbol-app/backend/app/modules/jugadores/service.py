from typing import List, Optional
from uuid import UUID

from injector import Inject

from app.modules.jugadores.models import Jugador
from app.modules.jugadores.repository import JugadorRepository
from app.modules.jugadores.schemas import JugadorCreate, JugadorUpdate
from app.services.base_crud_service import BaseService


class JugadorService(BaseService):
    def __init__(self, repo: Inject[JugadorRepository]) -> None:
        super().__init__(repo)

    def get_by_numero(self, numero: int) -> Optional[Jugador]:
        return self.repo.get_by_numero(numero)

    def get_activos(self) -> List[Jugador]:
        return self.repo.get_activos()
