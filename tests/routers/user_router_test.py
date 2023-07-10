from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from database import SessionLocal
from repositories.request_logs_repository import RequestLogRepository
from services.token_service import TokenService
from schemas.token_schema import TokenData
import uuid
from main import app
from services.user_service import UserService
from schemas.user_schema import (
    User,
    UserWithTokenResponse,
    UserLogin,
    UserBase,
    UserUpdate,
)
from sqlalchemy.orm import Session
from fastapi import HTTPException
from dependencies import get_db
client = TestClient(app)

def test_create_user_bad_request():
    mock_db = MagicMock(spec=Session)
    mock_user_service = MagicMock(spec=UserService)
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[UserService] = lambda db: mock_user_service

    mock_user_service.get_user.return_value = None
    with patch.object(RequestLogRepository, "create_request_log", return_value=None):
        with patch.object(TokenService, "verify_token", return_value=TokenData(user_id="asdasd", exp=24)):
            response = client.post("/users", json={})
            assert response.status_code == 422

def test_get_user_not_found():
    mock_db = MagicMock(spec=Session)
    mock_user_service = MagicMock(spec=UserService)
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[UserService] = lambda db: mock_user_service

    mock_user_service.get_user.return_value = None
    with patch.object(RequestLogRepository, "create_request_log", return_value=None):
        with patch.object(TokenService, "verify_token", return_value=TokenData(user_id="1ascaasdasdscasc", exp=24)):
            response = client.get("/users/1")
            assert response.status_code == 404
