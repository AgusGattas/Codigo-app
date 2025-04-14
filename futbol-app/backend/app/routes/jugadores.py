from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter(
    prefix="/jugadores",
    tags=["jugadores"]
)

@router.post("/", response_model=schemas.Jugador)
def crear_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    db_jugador = models.Jugador(**jugador.dict())
    db.add(db_jugador)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

@router.get("/", response_model=List[schemas.Jugador])
def obtener_jugadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jugadores = db.query(models.Jugador).offset(skip).limit(limit).all()
    return jugadores

@router.get("/{jugador_id}", response_model=schemas.Jugador)
def obtener_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@router.put("/{jugador_id}", response_model=schemas.Jugador)
def actualizar_jugador(jugador_id: int, jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    db_jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if db_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    
    for key, value in jugador.dict().items():
        setattr(db_jugador, key, value)
    
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

@router.delete("/{jugador_id}")
def eliminar_jugador(jugador_id: int, db: Session = Depends(get_db)):
    db_jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if db_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    
    db.delete(db_jugador)
    db.commit()
    return {"message": "Jugador eliminado"} 