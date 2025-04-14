from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter(
    prefix="/asignaciones",
    tags=["asignaciones"]
)

@router.post("/", response_model=schemas.Asignacion)
def crear_asignacion(asignacion: schemas.AsignacionCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva asignación.
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

@router.get("/jugador/{jugador_id}", response_model=List[schemas.Elemento])
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

@router.get("/pendientes", response_model=List[schemas.Asignacion])
def obtener_asignaciones_pendientes(db: Session = Depends(get_db)):
    """
    Obtiene todas las asignaciones pendientes.
    """
    asignaciones = db.query(models.Asignacion).filter(
        models.Asignacion.activo == True
    ).all()
    return asignaciones

@router.put("/devolver/{asignacion_id}")
def devolver_elemento(asignacion_id: int, db: Session = Depends(get_db)):
    """
    Marca una asignación como devuelta.
    """
    asignacion = db.query(models.Asignacion).filter(models.Asignacion.id == asignacion_id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    
    asignacion.activo = False
    db.commit()
    return {"message": "Elemento devuelto correctamente"}

@router.post("/rotate", response_model=List[schemas.AsignacionResponse])
def rotate_elementos(db: Session = Depends(get_db)):
    # Obtener asignaciones activas
    asignaciones_activas = db.query(models.Asignacion).filter(models.Asignacion.activo == True).all()
    
    # Obtener elementos activos
    elementos_activos = db.query(models.Elemento).filter(models.Elemento.activo == True).all()
    
    # Obtener jugadores activos
    jugadores_activos = db.query(models.Jugador).filter(models.Jugador.activo == True).all()
    
    if not elementos_activos or not jugadores_activos:
        raise HTTPException(status_code=400, detail="No hay elementos o jugadores activos para rotar")
    
    # Desactivar todas las asignaciones actuales
    for asignacion in asignaciones_activas:
        asignacion.activo = False
    
    # Crear nuevas asignaciones rotando los elementos
    nuevas_asignaciones = []
    num_jugadores = len(jugadores_activos)
    
    for i, elemento in enumerate(elementos_activos):
        jugador_index = i % num_jugadores
        nueva_asignacion = models.Asignacion(
            jugador_id=jugadores_activos[jugador_index].id,
            elemento_id=elemento.id,
            activo=True
        )
        nuevas_asignaciones.append(nueva_asignacion)
    
    # Agregar las nuevas asignaciones a la base de datos
    db.add_all(nuevas_asignaciones)
    db.commit()
    
    return nuevas_asignaciones 