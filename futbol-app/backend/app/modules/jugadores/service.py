from typing import List, Optional
from uuid import UUID

from injector import Inject

from app.modules.jugadores.models import Jugador
from app.modules.jugadores.repository import JugadorRepository
from app.modules.jugadores.schemas import JugadorCreate, JugadorUpdate
from app.services.base_crud_service import BaseService


class JugadorService(BaseService):
    def __init__(self, repo: Inject[JugadorRepository]):
        super().__init__(repo)

    def get_by_numero(self, numero: int) -> Optional[Jugador]:
        return self.repo.get_by_numero(numero)

    def get_activos(self) -> List[Jugador]:
        return self.repo.get_activos()

    def get_all(self) -> List[Jugador]:
        return self.repo.get_all()

    def get_by_id(self, jugador_id: int) -> Optional[Jugador]:
        return self.repo.get_by_id(jugador_id)

    def create(self, jugador_data: JugadorCreate) -> Jugador:
        jugador = Jugador(**jugador_data.model_dump())
        return self.repo.create(jugador)

    def update(self, jugador_id: int, jugador_data: JugadorCreate) -> Optional[Jugador]:
        jugador = self.repo.get_by_id(jugador_id)
        if jugador:
            for key, value in jugador_data.model_dump().items():
                setattr(jugador, key, value)
            return self.repo.update(jugador)
        return None

    def delete(self, jugador_id: int) -> bool:
        jugador = self.repo.get_by_id(jugador_id)
        if jugador:
            self.repo.delete(jugador)
            return True
        return False 