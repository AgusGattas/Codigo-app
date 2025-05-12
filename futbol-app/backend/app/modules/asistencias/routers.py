from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.modules.asistencias.service import AsistenciaService

router = APIRouter(
    prefix="/asistencias",
    tags=["asistencias"]
)

# @router.get("/", response_model=List[AsistenciaSchema])
# def get_asistencias(db: Session = Depends(get_db)):
#     service = AsistenciaService(db)
#     return service.get_all()

# @router.get("/jugador/{jugador_id}", response_model=List[AsistenciaSchema])
# def get_asistencias_jugador(jugador_id: int, db: Session = Depends(get_db)):
#     service = AsistenciaService(db)
#     return service.get_by_jugador(jugador_id)

# @router.get("/partido/{partido_id}", response_model=List[AsistenciaJugador])
# def get_asistencias_partido(partido_id: int, db: Session = Depends(get_db)):
#     service = AsistenciaService(db)
#     return service.get_by_partido(partido_id)

# @router.post("/", response_model=AsistenciaSchema)
# def create_asistencia(asistencia: AsistenciaCreate, db: Session = Depends(get_db)):
#     service = AsistenciaService(db)
#     return service.create(asistencia)

# @router.put("/{asistencia_id}", response_model=AsistenciaSchema)
# def update_asistencia(asistencia_id: int, asistencia: AsistenciaCreate, db: Session = Depends(get_db)):
#     service = AsistenciaService(db)
#     updated_asistencia = service.update(asistencia_id, asistencia)
#     if not updated_asistencia:
#         raise HTTPException(status_code=404, detail="Asistencia no encontrada")
#     return updated_asistencia

# @router.delete("/{asistencia_id}")
# def delete_asistencia(asistencia_id: int, db: Session = Depends(get_db)):
#     service = AsistenciaService(db)
#     if not service.delete(asistencia_id):
#         raise HTTPException(status_code=404, detail="Asistencia no encontrada")
#     return {"message": "Asistencia eliminada"} 