from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List

from schemas.request_log_schema import RequestLog
from services.analytics_service import AnalyticsService
from sqlalchemy.orm import Session
from dependencies import get_db
from models.permission_model import *
from routers.utils import has_permission

router = APIRouter()

@router.get("/request_logs", response_model=List[RequestLog])
async def get_request_logs(limit: int = 100, offset: int = 0, db: Session = Depends(get_db), requested_user=Depends(has_permission(ANALYTICS_API_LOG_PERMISSION))):
    analytics_service = AnalyticsService(db)
    request_logs = analytics_service.get_all_request_logs(requested_user, limit, offset)
    return request_logs