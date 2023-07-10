from typing import List
from sqlalchemy.orm import Session
from repositories.request_logs_repository import RequestLogRepository
from datetime import timedelta
from fastapi import HTTPException

TOKEN_EXPIRE_TIME_FOR_LOGIN = 1440  # 24 hours

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
        self.request_logs_repo = RequestLogRepository(db)

    def get_all_request_logs(self, requested_user, limit=None, offset=None):
        if not requested_user.is_admin():
            raise HTTPException(status_code=401, detail="Does not have permission to fetch logs")
        request_logs = self.request_logs_repo.get_all_request_logs(offset, limit)
        return request_logs