from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..models import models
from ..schemas.schemas import Partido, PartidoCreate
from ..database import get_db

router = APIRouter(
    prefix="/partidos",
    tags=["partidos"]
)

@router.post("/", response_model=Partido)
def crear_partido(partido: PartidoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo partido.
    """
    db_partido = models.Partido(**partido.dict())
    db.add(db_partido)
    db.commit()
    db.refresh(db_partido)
    return db_partido

@router.get("/", response_model=List[Partido])
def obtener_partidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene todos los partidos.
    """
    partidos = db.query(models.Partido).offset(skip).limit(limit).all()
    return partidos

@router.get("/{partido_id}", response_model=Partido)
def obtener_partido(partido_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un partido por su ID.
    """
    partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

@router.put("/{partido_id}", response_model=Partido)
def actualizar_partido(partido_id: int, partido: PartidoCreate, db: Session = Depends(get_db)):
    """
    Actualiza un partido existente.
    """
    db_partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if db_partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    
    for key, value in partido.dict().items():
        setattr(db_partido, key, value)
    
    db.commit()
    db.refresh(db_partido)
    return db_partido

@router.delete("/{partido_id}")
def eliminar_partido(partido_id: int, db: Session = Depends(get_db)):
    """
    Elimina un partido.
    """
    partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    
    db.delete(partido)
    db.commit()
    return {"message": "Partido eliminado correctamente"} 