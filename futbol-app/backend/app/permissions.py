from abc import ABC, abstractmethod

from fastapi import HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader
from fastapi_injector import Injected
from sqlalchemy import text

from app.context import get_request_context
from app.core.config import settings
from app.database.base import DatabaseResource


class BasePermission(ABC):
    """
    Abstract permission that all other Permissions must be inherited from.

    Defines basic error message, status & error codes.

    Upon initialization, calls abstract method  `has_required_permissions`
    which will be specific to concrete implementation of Permission class.

    You would write your permissions like this:

    .. code-block:: python

        class TeapotUserAgentPermission(BasePermission):

            def has_required_permissions(self, request: Request) -> bool:
                return request.headers.get('User-Agent') == "Teapot v1.0"

    """

    error_msg = "Forbidden."
    status_code = status.HTTP_403_FORBIDDEN

    @abstractmethod
    def has_required_permissions(self, request: Request, **kwargs) -> bool:
        ...

    def __init__(self, request: Request, **kwargs):
        if not self.has_required_permissions(request=request, **kwargs):
            raise HTTPException(status_code=self.status_code, detail=self.error_msg)


class PermissionsDependency:
    """
    Permission dependency that is used to define and check all the permission
    classes from one place inside route definition.

    Use it as an argument to FastAPI's `Depends` as follows:

    .. code-block:: python

        app = FastAPI()

        @app.get(
            "/teapot/",
            dependencies=[Depends(
                PermissionsDependency([TeapotUserAgentPermission]))]
        )
        async def teapot() -> dict:
            return {"teapot": True}
    """

    def __init__(self, permissions_classes: list):
        self.permissions_classes = permissions_classes

    def __call__(self, request: Request, **kwargs):
        for permission_class in self.permissions_classes:
            permission_class(request=request, **kwargs)


# class UserPermissionsDependency(PermissionsDependency):
#     def __call__(
#         self,
#         request: Request,
#         user_id: uuid.UUID = Depends(),
#         test: SeniorityService = Injected(SeniorityService),
#     ):
#         for permission_class in self.permissions_classes:
#             permission_class(request=request, user_service=test)


# class OrganizationPermission(BasePermission):
#     def has_required_permissions(self, request: Request, user_service: SeniorityService) -> bool:
#         print(user_service.get_all_seniorities(limit=1))
#         print(request.state.user_id)
#         return 1


def DisableRLS(db: DatabaseResource = Injected(DatabaseResource)):
    req_ctx = get_request_context()
    req_ctx.authenticated = False
    db.session.execute(
        text("SET LOCAL ROLE :role;").bindparams(role=settings.DB_ADMIN_ROLE),
    )


def check_internal_api_key(
    api_key_header: str = Security(APIKeyHeader(name="X-Echo-internal", auto_error=False)),
):
    if api_key_header != settings.ECHO_INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    req_ctx = get_request_context()
    req_ctx.authenticated = False
