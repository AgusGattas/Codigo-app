import sentry_sdk
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.core.config import settings
from app.core.middlewares.axiom import AxiomMiddleware

from .dependencies import DependencyInjector
from .routers import get_app_router, get_internal_app_router


def create_app(
    dp_injector: DependencyInjector = None,
    add_middlewares: bool = settings.ENVIRONMENT != "local",
) -> FastAPI:
    if dp_injector is None:
        dp_injector = DependencyInjector(
            db_url=settings.DB_URL,
            pool_size=settings.DB_POOL_SIZE
        )

    app = FastAPI()
    internal_app = FastAPI()

    dp_injector.setup_injections(app)
    dp_injector.setup_injections(internal_app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["content-disposition"],
    )

    router = APIRouter()
    app_router = get_app_router()

    app.mount("/internal", internal_app)

    internal_app_router = get_internal_app_router()
    internal_app.include_router(internal_app_router)

    @router.get("/health")
    def sanity_check():
        return "FastAPI running!"

    if add_middlewares:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT,
            traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
            profiles_sample_rate=settings.SENTRY_PROFILES_SAMPLE_RATE,
        )
        app.add_middleware(AxiomMiddleware)

    app.include_router(app_router)
    app.include_router(router)
    add_pagination(app)
    add_pagination(internal_app)
    return app


# Crear la instancia de la aplicación
app = create_app()
