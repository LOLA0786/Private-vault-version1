from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

EXEMPT_PATHS = {
    "/docs",
    "/openapi.json",
    "/redoc",
}

class RoleTenantMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        # Allow public endpoints
        if request.url.path in EXEMPT_PATHS:
            return await call_next(request)

        role = request.headers.get("X-Role")

        if not role:
            raise HTTPException(status_code=403, detail="Role required")

        request.state.role = role

        return await call_next(request)
