"""Module with the routers related to the estadisticas service"""

from copy import deepcopy
from typing import List
from uuid import UUID

from fastapi import APIRouter



router = APIRouter(prefix="/estadisticas", tags=["estadisticas"])


# @router.get(
#     "",
#     response_description="Get all statistics",
#     status_code=status.HTTP_200_OK,
#     summary="Get all statistics",
#     description="Retrieves all statistics with pagination and filtering support.",
# )
# def get_estadisticas(
#     estadistica_filter: EstadisticaFilter = FilterDepends(EstadisticaFilter),
#     pagination_params: Params = Depends(),
#     estadistica_service: EstadisticaService = Injected(EstadisticaService),
# ) -> Page[EstadisticaResponse]:
#     return estadistica_service.get_all(
#         pagination_params=pagination_params,
#         entity_filter=estadistica_filter,
#         response_model=EstadisticaResponse,
#     )


# @router.get(
#     "/{estadistica_id}",
#     response_description="Get a single statistic",
#     status_code=status.HTTP_200_OK,
#     summary="Get a statistic by ID",
#     description="Retrieves a single statistic based on the provided ID.",
# )
# def get_estadistica(
#     estadistica_id: UUID,
#     estadistica_service: EstadisticaService = Injected(EstadisticaService),
# ) -> EstadisticaResponse:
#     try:
#         return estadistica_service.get_by_id(estadistica_id)
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))


# @router.get(
#     "/jugador/{jugador_id}",
#     response_description="Get statistics by player",
#     status_code=status.HTTP_200_OK,
#     summary="Get statistics by player",
#     description="Retrieves all statistics for a specific player.",
# )
# def get_estadisticas_by_jugador(
#     jugador_id: UUID,
#     estadistica_service: EstadisticaService = Injected(EstadisticaService),
# ) -> List[EstadisticaResponse]:
#     return estadistica_service.get_by_jugador(jugador_id)


# @router.get(
#     "/partido/{partido_id}",
#     response_description="Get statistics by match",
#     status_code=status.HTTP_200_OK,
#     summary="Get statistics by match",
#     description="Retrieves all statistics for a specific match.",
# )
# def get_estadisticas_by_partido(
#     partido_id: UUID,
#     estadistica_service: EstadisticaService = Injected(EstadisticaService),
# ) -> List[EstadisticaResponse]:
#     return estadistica_service.get_by_partido(partido_id)


# @router.post(
#     "",
#     response_description="Create new statistic",
#     status_code=status.HTTP_201_CREATED,
#     summary="Create a new statistic",
#     description="Creates a new statistic with the provided details.",
# )
# def create_estadistica(
#     estadistica: EstadisticaCreate,
#     estadistica_service: EstadisticaService = Injected(EstadisticaService),
# ) -> EstadisticaResponse:
#     return estadistica_service.create(estadistica)


# @router.put(
#     "/{estadistica_id}",
#     response_description="Update statistic",
#     status_code=status.HTTP_200_OK,
#     summary="Update a statistic",
#     description="Updates the details of a statistic based on the provided ID.",
# )
# def update_estadistica(
#     estadistica_id: UUID,
#     estadistica: EstadisticaUpdate,
#     estadistica_service: EstadisticaService = Injected(EstadisticaService),
# ) -> EstadisticaResponse:
#     try:
#         return estadistica_service.update(estadistica_id, estadistica)
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))


# @router.delete(
#     "/{estadistica_id}",
#     response_description="Delete statistic",
#     status_code=status.HTTP_204_NO_CONTENT,
#     summary="Delete a statistic",
#     description="Deletes a statistic based on the provided ID.",
# )
# def delete_estadistica(
#     estadistica_id: UUID,
#     estadistica_service: EstadisticaService = Injected(EstadisticaService),
# ) -> None:
#     try:
#         estadistica_service.delete(estadistica_id)
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))


# # Internal routes
# internal_router = deepcopy(router)
# internal_router.prefix = "/internal/estadisticas"
# internal_router.tags = ["internal-estadisticas"]


# @internal_router.post(
#     "/bulk",
#     response_description="Create multiple statistics",
#     status_code=status.HTTP_201_CREATED,
#     summary="Create multiple statistics",
#     description="Creates multiple statistics with the provided details.",
# )
# def create_bulk_estadisticas(
#     estadisticas: List[EstadisticaCreate],
#     estadistica_service: EstadisticaService = Injected(EstadisticaService),
# ) -> List[EstadisticaResponse]:
#     return estadistica_service.create_bulk(estadisticas)


# @internal_router.delete(
#     "/jugador/{jugador_id}",
#     response_description="Delete all statistics for a player",
#     status_code=status.HTTP_204_NO_CONTENT,
#     summary="Delete all statistics for a player",
#     description="Deletes all statistics for a specific player.",
# )
# def delete_estadisticas_by_jugador(
#     jugador_id: UUID,
#     estadistica_service: EstadisticaService = Injected(EstadisticaService),
# ) -> None:
#     try:
#         estadistica_service.delete_by_jugador(jugador_id)
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))


# @internal_router.delete(
#     "/partido/{partido_id}",
#     response_description="Delete all statistics for a match",
#     status_code=status.HTTP_204_NO_CONTENT,
#     summary="Delete all statistics for a match",
#     description="Deletes all statistics for a specific match.",
# )
# def delete_estadisticas_by_partido(
#     partido_id: UUID,
#     estadistica_service: EstadisticaService = Injected(EstadisticaService),
# ) -> None:
#     try:
#         estadistica_service.delete_by_partido(partido_id)
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e)) 