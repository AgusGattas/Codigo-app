from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter(
    prefix="/estadisticas",
    tags=["estadisticas"]
)

# Endpoints para Partidos
@router.post("/partidos/", response_model=schemas.Partido)
def crear_partido(partido: schemas.PartidoCreate, db: Session = Depends(get_db)):
    db_partido = models.Partido(**partido.dict())
    db.add(db_partido)
    db.commit()
    db.refresh(db_partido)
    return db_partido

@router.get("/partidos/", response_model=List[schemas.Partido])
def obtener_partidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Partido).offset(skip).limit(limit).all()

@router.get("/partidos/{partido_id}", response_model=schemas.EstadisticasPartido)
def obtener_partido(partido_id: int, db: Session = Depends(get_db)):
    partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    
    estadisticas = db.query(models.Estadistica).filter(
        models.Estadistica.partido_id == partido_id
    ).all()
    
    return {
        "partido_id": partido.id,
        "fecha": partido.fecha,
        "rival": partido.rival,
        "resultado_local": partido.resultado_local,
        "resultado_visitante": partido.resultado_visitante,
        "lugar": partido.lugar,
        "tipo": partido.tipo,
        "jugadores": estadisticas
    }

# Endpoints para Estadísticas
@router.post("/registro/", response_model=schemas.Estadistica)
def registrar_estadistica(estadistica: schemas.EstadisticaCreate, db: Session = Depends(get_db)):
    db_estadistica = models.Estadistica(**estadistica.dict())
    db.add(db_estadistica)
    db.commit()
    db.refresh(db_estadistica)
    return db_estadistica

@router.get("/jugadores/{jugador_id}", response_model=schemas.EstadisticasJugador)
def obtener_estadisticas_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    
    stats = db.query(
        func.count(models.Estadistica.partido_id).label('total_partidos'),
        func.sum(models.Estadistica.goles).label('total_goles'),
        func.sum(models.Estadistica.asistencias).label('total_asistencias'),
        func.sum(models.Estadistica.tarjetas_amarillas).label('total_amarillas'),
        func.sum(models.Estadistica.tarjetas_rojas).label('total_rojas'),
        func.sum(models.Estadistica.minutos_jugados).label('minutos_totales')
    ).filter(models.Estadistica.jugador_id == jugador_id).first()

    return {
        "jugador_id": jugador.id,
        "nombre_jugador": jugador.nombre,
        "total_partidos": stats.total_partidos or 0,
        "total_goles": stats.total_goles or 0,
        "total_asistencias": stats.total_asistencias or 0,
        "total_amarillas": stats.total_amarillas or 0,
        "total_rojas": stats.total_rojas or 0,
        "minutos_totales": stats.minutos_totales or 0,
        "promedio_minutos": (stats.minutos_totales or 0) / (stats.total_partidos or 1)
    }

@router.get("/resumen/", response_model=List[schemas.EstadisticasJugador])
def obtener_resumen_estadisticas(
    db: Session = Depends(get_db),
    min_goles: int = None,
    min_asistencias: int = None,
    min_partidos: int = None,
    min_minutos: int = None,
    max_amarillas: int = None,
    max_rojas: int = None,
    ordenar_por: str = None,
    orden: str = "desc"  # "asc" o "desc"
):
    """
    Obtiene un resumen de estadísticas para todos los jugadores con filtros opcionales.
    
    Parámetros:
    - min_goles: Mínimo de goles requeridos
    - min_asistencias: Mínimo de asistencias requeridas
    - min_partidos: Mínimo de partidos jugados requeridos
    - min_minutos: Mínimo de minutos jugados requeridos
    - max_amarillas: Máximo de tarjetas amarillas permitidas
    - max_rojas: Máximo de tarjetas rojas permitidas
    - ordenar_por: Campo por el cual ordenar (goles, asistencias, partidos, minutos, amarillas, rojas)
    - orden: Orden de clasificación ("asc" o "desc")
    """
    # Obtener todos los jugadores
    jugadores = db.query(models.Jugador).all()
    
    resumen = []
    for jugador in jugadores:
        # Obtener estadísticas solo de partidos donde jugó (minutos > 0)
        estadisticas = db.query(models.Estadistica).filter(
            models.Estadistica.jugador_id == jugador.id,
            models.Estadistica.minutos_jugados > 0  # Solo contar partidos donde jugó
        ).all()
        
        if not estadisticas:  # Si no tiene partidos jugados, no lo incluimos
            continue
            
        total_partidos = len(estadisticas)
        total_goles = sum(e.goles for e in estadisticas)
        total_asistencias = sum(e.asistencias for e in estadisticas)
        total_amarillas = sum(e.tarjetas_amarillas for e in estadisticas)
        total_rojas = sum(e.tarjetas_rojas for e in estadisticas)
        total_minutos = sum(e.minutos_jugados for e in estadisticas)
        promedio_minutos = total_minutos / total_partidos if total_partidos > 0 else 0
        
        # Aplicar filtros
        if min_goles is not None and total_goles < min_goles:
            continue
        if min_asistencias is not None and total_asistencias < min_asistencias:
            continue
        if min_partidos is not None and total_partidos < min_partidos:
            continue
        if min_minutos is not None and total_minutos < min_minutos:
            continue
        if max_amarillas is not None and total_amarillas > max_amarillas:
            continue
        if max_rojas is not None and total_rojas > max_rojas:
            continue
        
        resumen.append(schemas.EstadisticasJugador(
            jugador_id=jugador.id,
            nombre_jugador=jugador.nombre,
            total_partidos=total_partidos,
            total_goles=total_goles,
            total_asistencias=total_asistencias,
            total_amarillas=total_amarillas,
            total_rojas=total_rojas,
            minutos_totales=total_minutos,
            promedio_minutos=promedio_minutos
        ))
    
    # Ordenar el resumen si se especifica un campo
    if ordenar_por:
        campos_ordenamiento = {
            "goles": lambda x: x.total_goles,
            "asistencias": lambda x: x.total_asistencias,
            "partidos": lambda x: x.total_partidos,
            "minutos": lambda x: x.minutos_totales,
            "amarillas": lambda x: x.total_amarillas,
            "rojas": lambda x: x.total_rojas,
            "promedio_minutos": lambda x: x.promedio_minutos
        }
        
        if ordenar_por in campos_ordenamiento:
            resumen.sort(
                key=campos_ordenamiento[ordenar_por],
                reverse=(orden.lower() == "desc")
            )
    
    return resumen

@router.put("/partidos/{partido_id}", response_model=schemas.Partido)
def actualizar_partido(
    partido_id: int,
    partido_actualizado: schemas.PartidoCreate,
    db: Session = Depends(get_db)
):
    db_partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if db_partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    
    for key, value in partido_actualizado.dict().items():
        setattr(db_partido, key, value)
    
    db.commit()
    db.refresh(db_partido)
    return db_partido

@router.delete("/partidos/{partido_id}")
def eliminar_partido(partido_id: int, db: Session = Depends(get_db)):
    db_partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if db_partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    
    # Eliminar todas las estadísticas asociadas al partido
    db.query(models.Estadistica).filter(
        models.Estadistica.partido_id == partido_id
    ).delete()
    
    # Eliminar el partido
    db.delete(db_partido)
    db.commit()
    return {"message": "Partido y estadísticas asociadas eliminados"}

@router.post("/registro-multiple/", response_model=List[schemas.Estadistica])
def registrar_estadisticas_multiple(estadisticas: List[schemas.EstadisticaCreate], db: Session = Depends(get_db)):
    db_estadisticas = []
    for estadistica in estadisticas:
        db_estadistica = models.Estadistica(**estadistica.dict())
        db.add(db_estadistica)
        db_estadisticas.append(db_estadistica)
    db.commit()
    for estadistica in db_estadisticas:
        db.refresh(estadistica)
    return db_estadisticas 