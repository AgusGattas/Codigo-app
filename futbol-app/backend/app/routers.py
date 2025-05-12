"""Module for including all the app's routers"""

import logging
from fastapi import APIRouter

from app.modules.jugadores.routers import router as jugadores_router
from app.modules.partidos.routers import router as partidos_router
from app.modules.estadisticas.routers import router as estadisticas_router
from app.modules.asistencias.routers import router as asistencias_router

logger = logging.getLogger(__name__)


def get_app_router():
    router = APIRouter()

    # Jugadores
    router.include_router(
        jugadores_router,
        prefix="/jugadores",
        tags=["jugadores"],
    )

    # Partidos
    router.include_router(
        partidos_router,
        prefix="/partidos",
        tags=["partidos"],
    )

    # Estadísticas
    router.include_router(
        estadisticas_router,
        prefix="/estadisticas",
        tags=["estadisticas"],
    )

    # Asistencias
    router.include_router(
        asistencias_router,
        prefix="/asistencias",
        tags=["asistencias"],
    )

    return router


def get_internal_app_router():
    router = APIRouter()
    return router


def dump_router(router: APIRouter):
    def tabulate(data):
        # Get all headers (keys) from the first dictionary
        headers = data[0].keys()

        # Calculate the maximum width of each column by iterating over each key and value
        col_widths = {
            key: max(len(str(key)), max(len(str(row[key])) for row in data)) for key in headers
        }

        # Print the headers
        header_row = " ".join(f"{key.upper():<{col_widths[key]}}" for key in headers)
        print(header_row)

        # Print each row of data
        for row in data:
            row_str = " ".join(f"{str(row[key]):<{col_widths[key]}}" for key in headers)
            print(row_str)

    def route_scopes(route):
        if not route.dependencies:
            return ""

        scopes = []
        for dependency in route.dependencies:
            if hasattr(dependency, "rbac_scopes"):
                scopes.extend(dependency.rbac_scopes)

        return ", ".join(map(str, scopes))

    data = []

    try:
        for route in router.routes:
            for method in route.methods:
                data.append(
                    {
                        "method": method,
                        "path": route.path,
                        "handler": route.endpoint.__module__ + "." + route.endpoint.__name__,
                        "tags": route.tags,
                        "permissions": route_scopes(route),
                    }
                )

        tabulate(data)
    except Exception:
        # We don't want to fail or obscure the actual error if we fail to dump
        # the router, so we just print the error and move on
        logger.exception("Failed to dump router")
