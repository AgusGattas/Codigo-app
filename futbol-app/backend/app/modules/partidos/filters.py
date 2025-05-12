from sqlalchemy import or_
from app.modules.partidos.models import Partido
from datetime import datetime

class PartidoFilters:
    @staticmethod
    def apply_filters(query, filters: dict):
        if filters.get('search'):
            search = f"%{filters['search']}%"
            query = query.filter(
                or_(
                    Partido.rival.ilike(search),
                    Partido.lugar.ilike(search)
                )
            )
        
        if filters.get('tipo'):
            query = query.filter(Partido.tipo == filters['tipo'])
            
        if filters.get('fecha_inicio'):
            query = query.filter(Partido.fecha >= filters['fecha_inicio'])
            
        if filters.get('fecha_fin'):
            query = query.filter(Partido.fecha <= filters['fecha_fin'])
            
        return query 