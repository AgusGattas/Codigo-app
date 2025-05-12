from sqlalchemy import and_
from app.modules.asistencias.models import Asistencia

class AsistenciaFilters:
    @staticmethod
    def apply_filters(query, filters: dict):
        if filters.get('jugador_id'):
            query = query.filter(Asistencia.jugador_id == filters['jugador_id'])
            
        if filters.get('partido_id'):
            query = query.filter(Asistencia.partido_id == filters['partido_id'])
            
        if filters.get('presente') is not None:
            query = query.filter(Asistencia.presente == filters['presente'])
            
        if filters.get('justificacion'):
            query = query.filter(Asistencia.justificacion.ilike(f"%{filters['justificacion']}%"))
            
        return query 