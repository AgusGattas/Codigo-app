from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import models
from ..schemas import schemas
from datetime import date

router = APIRouter(
    prefix="/elementos",
    tags=["elementos"]
)

@router.post("/", response_model=schemas.Elemento)
def crear_elemento(elemento: schemas.ElementoCreate, db: Session = Depends(get_db)):
    db_elemento = models.Elemento(**elemento.dict())
    db.add(db_elemento)
    db.commit()
    db.refresh(db_elemento)
    return db_elemento

@router.get("/", response_model=List[schemas.Elemento])
def obtener_elementos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    elementos = db.query(models.Elemento).offset(skip).limit(limit).all()
    return elementos

@router.post("/asignar", response_model=schemas.Asignacion)
def asignar_elemento(asignacion: schemas.AsignacionCreate, db: Session = Depends(get_db)):
    """
    Asigna un elemento a un jugador.
    """
    # Verificar que el jugador y el elemento existan
    jugador = db.query(models.Jugador).filter(models.Jugador.id == asignacion.jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    
    elemento = db.query(models.Elemento).filter(models.Elemento.id == asignacion.elemento_id).first()
    if not elemento:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    
    # Verificar si ya existe una asignación activa
    asignacion_existente = db.query(models.Asignacion).filter(
        models.Asignacion.jugador_id == asignacion.jugador_id,
        models.Asignacion.elemento_id == asignacion.elemento_id,
        models.Asignacion.activo == True
    ).first()
    
    if asignacion_existente:
        raise HTTPException(status_code=400, detail="El jugador ya tiene asignado este elemento")
    
    # Crear nueva asignación
    db_asignacion = models.Asignacion(**asignacion.dict())
    db.add(db_asignacion)
    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion

@router.delete("/desasignar/{jugador_id}/{elemento_id}")
def desasignar_elemento(jugador_id: int, elemento_id: int, db: Session = Depends(get_db)):
    """
    Desasigna un elemento de un jugador.
    """
    asignacion = db.query(models.Asignacion).filter(
        models.Asignacion.jugador_id == jugador_id,
        models.Asignacion.elemento_id == elemento_id,
        models.Asignacion.activo == True
    ).first()
    
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    
    asignacion.activo = False
    db.commit()
    return {"message": "Elemento desasignado correctamente"}

@router.get("/asignaciones/{jugador_id}", response_model=List[schemas.Elemento])
def obtener_elementos_asignados(jugador_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los elementos asignados a un jugador.
    """
    asignaciones = db.query(models.Asignacion).filter(
        models.Asignacion.jugador_id == jugador_id,
        models.Asignacion.activo == True
    ).all()
    
    elementos = [asignacion.elemento for asignacion in asignaciones]
    return elementos

@router.put("/devolver/{asignacion_id}")
def devolver_elemento(asignacion_id: int, db: Session = Depends(get_db)):
    asignacion = db.query(models.ElementoAsignado).filter(models.ElementoAsignado.id == asignacion_id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    
    asignacion.devuelto = True
    asignacion.fecha_devolucion = date.today()
    db.commit()
    return {"message": "Elemento devuelto exitosamente"}

@router.get("/asignaciones/pendientes", response_model=List[schemas.ElementoAsignado])
def obtener_asignaciones_pendientes(db: Session = Depends(get_db)):
    asignaciones = db.query(models.ElementoAsignado).filter(
        models.ElementoAsignado.devuelto == False
    ).all()
    return asignaciones 