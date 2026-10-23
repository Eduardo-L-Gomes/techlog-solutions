from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

class AuthenticationToken(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("session_token")

        if token != "token-valido":
            return RedirectResponse(url="/login", status_code=303)

        return await call_next(request)