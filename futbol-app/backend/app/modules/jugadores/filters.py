from sqlalchemy import or_
from app.modules.jugadores.models import Jugador
from fastapi_filter.contrib.sqlalchemy import Filter


class JugadorFilters(Filter):
    nombre: str | None = None
    apellido: str | None = None
    activo: bool | None = None
    numero: int | None = None
    
    class Constants(Filter.Constants):
        model = Jugador
        