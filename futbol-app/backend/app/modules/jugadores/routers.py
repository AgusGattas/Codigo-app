from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()

# @router.get("/", response_model=List[Jugador])
# def get_jugadores(
#     db: Session = Depends(get_db),
#     search: str = None,
#     activo: bool = None,
#     numero: int = None
# ):
#     service = JugadorService(db)
#     filters = {
#         'search': search,
#         'activo': activo,
#         'numero': numero
#     }
#     jugadores = service.get_all()
#     return JugadorFilters.apply_filters(jugadores, filters).all()

# @router.post("/", response_model=Jugador)
# def create_jugador(jugador: JugadorCreate, db: Session = Depends(get_db)):
#     service = JugadorService(db)
#     return service.create(jugador)

# @router.get("/{jugador_id}", response_model=Jugador)
# def get_jugador(jugador_id: int, db: Session = Depends(get_db)):
#     service = JugadorService(db)
#     jugador = service.get_by_id(jugador_id)
#     if not jugador:
#         raise HTTPException(status_code=404, detail="Jugador no encontrado")
#     return jugador

# @router.put("/{jugador_id}", response_model=Jugador)
# def update_jugador(jugador_id: int, jugador: JugadorCreate, db: Session = Depends(get_db)):
#     service = JugadorService(db)
#     updated_jugador = service.update(jugador_id, jugador)
#     if not updated_jugador:
#         raise HTTPException(status_code=404, detail="Jugador no encontrado")
#     return updated_jugador

# @router.delete("/{jugador_id}")
# def delete_jugador(jugador_id: int, db: Session = Depends(get_db)):
#     service = JugadorService(db)
#     if not service.delete(jugador_id):
#         raise HTTPException(status_code=404, detail="Jugador no encontrado")
#     return {"message": "Jugador eliminado"} 