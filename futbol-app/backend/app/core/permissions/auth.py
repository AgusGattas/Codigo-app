from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.context import get_request_context
from app.core.config import settings


class AuthenticatedUser:
    @classmethod
    def current_user_id(
        cls,
        request: Request,
        http_auth: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    ) -> str:
        return getattr(request.state, "user_id", cls.get_user_id(request, http_auth))

    @classmethod
    def get_user_id(
        cls,
        request: Request,
        http_auth: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    ) -> str:
        try:
            payload = jwt.decode(
                http_auth.credentials,
                settings.AUTH_JWT_SECRET,
                algorithms=["HS256"],
                audience="authenticated",
            )

            req_ctx = get_request_context()
            req_ctx.jwt = payload
            req_ctx.user_id = payload.get("sub")

            request.state.user_id = payload.get("sub")
            request.state.email = payload.get("email")
            return payload.get("sub")
        except (JWTError, AttributeError):
            raise HTTPException(  # noqa: B904
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
