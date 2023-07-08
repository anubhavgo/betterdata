from fastapi import Request, HTTPException
from jose import jwt
from services.token_service import TokenService
from fastapi.responses import JSONResponse

EXCLUDED_URLS = [("/users","POST"),("/users/login","POST")]

class AuthMiddleware:
    def __init__(self, app):
        self.app = app
        self.token_service = TokenService()

    async def __call__(self, request: Request, call_next):
        # Exclude specific routes from token verification if needed
        for path, method in EXCLUDED_URLS:
            if request.url.path == path and request.method == method:
                return await call_next(request)
        try:
            token = request.headers.get("Authorization", "").split("Bearer ")[-1]
            token_data = self.token_service.verify_token(token)
            request.state.user_id = token_data.user_id
            response = await call_next(request)
            return response
        except HTTPException as ex:
            return JSONResponse(status_code=ex.status_code, content={"detail": ex.detail})