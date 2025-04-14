from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import models
from ..schemas import schemas
from datetime import date

router = APIRouter(
    prefix="/asistencias",
    tags=["asistencias"]
)

@router.post("/", response_model=schemas.Asistencia)
def registrar_asistencia(asistencia: schemas.AsistenciaCreate, db: Session = Depends(get_db)):
    # Verificar si el jugador existe
    jugador = db.query(models.Jugador).filter(models.Jugador.id == asistencia.jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    
    db_asistencia = models.Asistencia(**asistencia.dict())
    db.add(db_asistencia)
    db.commit()
    db.refresh(db_asistencia)
    return db_asistencia

@router.get("/", response_model=List[schemas.Asistencia])
def obtener_asistencias(
    fecha: date = None,
    tipo: schemas.TipoEvento = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Asistencia)
    
    if fecha:
        query = query.filter(models.Asistencia.fecha == fecha)
    if tipo:
        query = query.filter(models.Asistencia.tipo == tipo)
    
    return query.all()

@router.get("/jugador/{jugador_id}", response_model=List[schemas.Asistencia])
def obtener_asistencias_jugador(jugador_id: int, db: Session = Depends(get_db)):
    asistencias = db.query(models.Asistencia).filter(
        models.Asistencia.jugador_id == jugador_id
    ).all()
    return asistencias

@router.put("/{asistencia_id}", response_model=schemas.Asistencia)
def actualizar_asistencia(
    asistencia_id: int,
    asistencia: schemas.AsistenciaCreate,
    db: Session = Depends(get_db)
):
    db_asistencia = db.query(models.Asistencia).filter(models.Asistencia.id == asistencia_id).first()
    if not db_asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    
    for key, value in asistencia.dict().items():
        setattr(db_asistencia, key, value)
    
    db.commit()
    db.refresh(db_asistencia)
    return db_asistencia 