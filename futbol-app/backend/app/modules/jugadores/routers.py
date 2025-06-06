from fastapi import APIRouter, status, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.modules.jugadores.schemas import JugadorCreate, JugadorResponse
from app.modules.jugadores.service import JugadorService
from fastapi_injector import Injected
from app.modules.jugadores.filters import JugadorFilters
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, Params
from app.core.permissions.auth import AuthenticatedUser
from fastapi import BackgroundTasks
from app.modules.jugadores.schemas import JugadorUpdate

router = APIRouter()


@router.post(
    "",
    response_description="Create player",
    status_code=status.HTTP_201_CREATED,
)
def create_player(
    player: JugadorCreate = Body(...),
    player_service: JugadorService = Injected(JugadorService),
) -> JugadorResponse:
    return player_service.create(player)

@router.get(
    "",
    response_description="Get all the created entities",
    status_code=status.HTTP_200_OK,
)
def get_all_players(
    player_filter: JugadorFilters = FilterDepends(JugadorFilters),
    player_service: JugadorService = Injected(JugadorService),
    pagination_params: Params = Depends(),
) -> Page[JugadorResponse]:
    return player_service.get_all(
        player_filter=player_filter,
        pagination_params=pagination_params,
        response_model=JugadorResponse,
    )

@router.get(
    "/{player_id}",
    response_description="Get a player by id",
    status_code=status.HTTP_200_OK,
)
def get_player_by_id(player_id: UUID, player_service: JugadorService = Injected(JugadorService)):
    player = player_service.get_by_id(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return player

@router.get(
    "/me",
    summary="Get your player profile",
    status_code=status.HTTP_200_OK,
)
def get_your_player_profile(
    player_id: UUID = Depends(AuthenticatedUser.current_user_id),
    player_service: JugadorService = Injected(JugadorService),
) -> JugadorResponse:
    return get_player_by_id(player_id, player_service)


@router.patch(
    "/{player_id}",
    response_description="Update player",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a player",
    description="Updates the details of a player based on the provided player ID. The updated player details should be provided in the request body.",
)
def update_player(
    player_id: UUID,
    player: JugadorUpdate = Body(...),
    player_service: JugadorService = Injected(JugadorService),
) -> None:
    player_service.update(player_id, player)

@router.delete(
    "/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete player",
    summary="Delete a player",
    description="Deletes a player based on the provided player ID.",
)
def delete_player(
    player_id: UUID,
    player_service: JugadorService = Injected(JugadorService),
) -> None:
    player_service.delete(player_id)
