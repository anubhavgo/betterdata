from starlette.middleware.base import BaseHTTPMiddleware
from models.request_log_model import RequestLog
from repositories.request_logs_repository import RequestLogRepository
from database import SessionLocal

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self,app):
        super().__init__(app)
        self.req_log_repo = RequestLogRepository(SessionLocal())

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        try:
            user_id = request.state.user_id
        except Exception:
            user_id = ''
        log_entry = RequestLog(method=request.method, url=str(request.url), 
                               status_code=response.status_code, user_id=user_id)
        self.req_log_repo.create_request_log(log_entry)
        return response