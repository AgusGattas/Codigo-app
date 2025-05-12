from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Optional
from app.modules.estadisticas.models import Estadistica

class EstadisticaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Estadistica]:
        return self.db.query(Estadistica).all()

    def get_by_id(self, estadistica_id: int) -> Optional[Estadistica]:
        return self.db.query(Estadistica).filter(Estadistica.id == estadistica_id).first()

    def get_by_partido(self, partido_id: int) -> List[Estadistica]:
        return self.db.query(Estadistica).filter(Estadistica.partido_id == partido_id).all()

    def get_by_jugador(self, jugador_id: int) -> List[Estadistica]:
        return self.db.query(Estadistica).filter(Estadistica.jugador_id == jugador_id).all()

    def create(self, estadistica: Estadistica) -> Estadistica:
        self.db.add(estadistica)
        self.db.commit()
        self.db.refresh(estadistica)
        return estadistica

    def update(self, estadistica: Estadistica) -> Estadistica:
        self.db.commit()
        self.db.refresh(estadistica)
        return estadistica

    def delete(self, estadistica: Estadistica) -> None:
        self.db.delete(estadistica)
        self.db.commit()

    def get_resumen_jugadores(self) -> List[Dict]:
        return self.db.query(
            Estadistica.jugador_id,
            func.count(Estadistica.id).label('total_partidos'),
            func.sum(Estadistica.goles).label('total_goles'),
            func.sum(Estadistica.asistencias).label('total_asistencias'),
            func.sum(Estadistica.tarjetas_amarillas).label('total_amarillas'),
            func.sum(Estadistica.tarjetas_rojas).label('total_rojas'),
            func.sum(Estadistica.minutos_jugados).label('minutos_totales'),
            func.avg(Estadistica.minutos_jugados).label('promedio_minutos')
        ).group_by(Estadistica.jugador_id).all() 