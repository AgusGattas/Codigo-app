from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime


router = APIRouter()

# @router.get("/", response_model=List[Partido])
# def get_partidos(
#     db: Session = Depends(get_db),
#     search: str = None,
#     tipo: str = None,
#     fecha_inicio: datetime = None,
#     fecha_fin: datetime = None
# ):
#     service = PartidoService(db)
#     filters = {
#         'search': search,
#         'tipo': tipo,
#         'fecha_inicio': fecha_inicio,
#         'fecha_fin': fecha_fin
#     }
#     partidos = service.get_all()
#     return PartidoFilters.apply_filters(partidos, filters).all()

# @router.post("/", response_model=Partido)
# def create_partido(partido: PartidoCreate, db: Session = Depends(get_db)):
#     service = PartidoService(db)
#     return service.create(partido)

# @router.get("/{partido_id}", response_model=PartidoWithStats)
# def get_partido(partido_id: int, db: Session = Depends(get_db)):
#     service = PartidoService(db)
#     partido = service.get_by_id(partido_id)
#     if not partido:
#         raise HTTPException(status_code=404, detail="Partido no encontrado")
#     return partido

# @router.put("/{partido_id}", response_model=Partido)
# def update_partido(partido_id: int, partido: PartidoCreate, db: Session = Depends(get_db)):
#     service = PartidoService(db)
#     updated_partido = service.update(partido_id, partido)
#     if not updated_partido:
#         raise HTTPException(status_code=404, detail="Partido no encontrado")
#     return updated_partido

# @router.delete("/{partido_id}")
# def delete_partido(partido_id: int, db: Session = Depends(get_db)):
#     service = PartidoService(db)
#     if not service.delete(partido_id):
#         raise HTTPException(status_code=404, detail="Partido no encontrado")
#     return {"message": "Partido eliminado"} 