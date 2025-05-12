from sqlalchemy import or_
from app.modules.jugadores.models import Jugador

class JugadorFilters:
    @staticmethod
    def apply_filters(query, filters: dict):
        if filters.get('search'):
            search = f"%{filters['search']}%"
            query = query.filter(
                or_(
                    Jugador.nombre.ilike(search),
                    Jugador.apellido.ilike(search)
                )
            )
        
        if filters.get('activo') is not None:
            query = query.filter(Jugador.activo == filters['activo'])
            
        if filters.get('numero'):
            query = query.filter(Jugador.numero == filters['numero'])
            
        return query 