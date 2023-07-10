from datetime import datetime, timedelta
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import uuid
from services.user_service import UserService
from repositories.user_repository import UserRepository
from services.token_service import TokenService
from schemas.user_schema import (
    User,
    UserUpdate
)

def test_create_user():
    mock_db = MagicMock()
    mock_user_repo = MagicMock()
    mock_token_service = MagicMock()
    
    user_service = UserService(mock_db)
    user_service.user_repo = mock_user_repo
    user_service.token_service = mock_token_service

    user = User(
        first_name="Hanan",
        last_name="Mehmood",
        gender="male",
        email="hanan.mehmood@betterdata.ai",
        phone="+123123123",
        username="somethingNice",
        password="9uQFF1Lh",
        birth_date="2010-12-25",
        avatar="img_url_such_as_gravatar",
        addresses=[ {
            "address": "1745 T Street Southeast",
            "city": "Washington",
            "postal_code": "20020",
            "state": "DC",
            "primary": True,
            "label":"home"
        }],
        status="active"
    )
    mock_user_repo.get_password_hash.return_value = "hashed_password"
    new_user = User(
        id=uuid.uuid4(),
        first_name="Hanan",
        last_name="Mehmood",
        gender="male",
        email="hanan.mehmood@betterdata.ai",
        phone="+123123123",
        username="somethingNice",
        password_hash="hashed_password",
        birth_date="2010-12-25",
        avatar="img_url_such_as_gravatar",
        addresses=[ {
            "address": "1745 T Street Southeast",
            "city": "Washington",
            "postal_code": "20020",
            "state": "DC",
            "primary": True,
            "label":"home"
        }],
        status="active"
    )
    mock_user_repo.create_user.return_value = new_user
    mock_token_service.create_access_token.return_value = "access_token"
    
    response = user_service.create_user(user)
    
    assert response.first_name == user.first_name
    assert response.token == "access_token"

def test_get_all_users():
    mock_db = MagicMock()
    mock_user_repo = MagicMock()
    
    user_service = UserService(mock_db)
    user_service.user_repo = mock_user_repo

    mock_requested_user = MagicMock()
    mock_requested_user.is_admin.return_value = True

    mock_user_repo.get_all_users.return_value = [
        User(
            id=uuid.uuid4(),
            first_name="Hanan",
            last_name="Mehmood",
            gender="male",
            email="hanan.mehmood@betterdata.ai",
            phone="+123123123",
            username="somethingNice",
            password_hash="hashed_password",
            birth_date="2010-12-25",
            avatar="img_url_such_as_gravatar",
            addresses=[],
            status="active"
        ),
        User(
            id=uuid.uuid4(),
            first_name="Hanan",
            last_name="Mehmood",
            gender="male",
            email="hanan.mehmood2@betterdata.ai",
            phone="+123123123",
            username="somethingNice2",
            password_hash="hashed_password",
            birth_date="2010-12-25",
            avatar="img_url_such_as_gravatar",
            addresses=[],
            status="active"
        ),
    ]
    
    response = user_service.get_all_users(mock_requested_user)
    
    assert len(response) == 2
    assert response[0].email == "hanan.mehmood@betterdata.ai"
    assert response[1].email == "hanan.mehmood2@betterdata.ai"

def test_get_user():
    mock_db = MagicMock()
    mock_user_repo = MagicMock()
    
    user_service = UserService(mock_db)
    user_service.user_repo = mock_user_repo

    mock_user_repo.get_user_by_id.return_value = User(
        id=uuid.uuid4(),
        first_name="Hanan",
        last_name="Mehmood",
        gender="male",
        email="hanan.mehmood2@betterdata.ai",
        phone="+123123123",
        username="somethingNice2",
        password_hash="hashed_password",
        birth_date="2010-12-25",
        avatar="img_url_such_as_gravatar",
        addresses=[],
        status="active"
    )
    
    response = user_service.get_user("34404058-a66b-489f-9aa6-65cc53d08c48")
    
    assert response.email == "hanan.mehmood2@betterdata.ai"

def test_update_user():
    mock_db = MagicMock()
    mock_user_repo = MagicMock()

    user_service = UserService(mock_db)
    user_service.user_repo = mock_user_repo

    mock_requested_user = MagicMock()
    mock_requested_user.is_admin.return_value = True

    user_update = UserUpdate(
        first_name="Hanan",
        last_name="Mehmood",
        gender="male",
        email="hanan.mehmood2@betterdata.ai",
        phone="+123123123",
        username="somethingNice2",
        password_hash="hashed_password",
        birth_date="2010-12-25",
        avatar="img_url_such_as_gravatar",
        addresses=[],
        status="active"
    )
    user_id = uuid.uuid4()
    mock_user_repo.update_user.return_value = User(
        id=user_id,
        first_name="Test",
        last_name="User",
        gender="male",
        email="hanan.mehmood2@betterdata.ai",
        phone="+123123123",
        username="somethingNice2",
        password_hash="hashed_password",
        birth_date="2010-12-25",
        avatar="img_url_such_as_gravatar",
        addresses=[],
        status="active"
    )

    response = user_service.update_user(mock_requested_user, user_update, user_id)

    assert response.first_name == "Test"
    assert response.last_name == "User"

def test_is_same_user_or_admin():
    mock_user = MagicMock()
    mock_user.is_admin.return_value = True
    mock_user.id = uuid.uuid4()

    user_service = UserService(None)
    result = user_service.is_same_user_or_admin(mock_user,uuid.uuid4())

    assert result is True

    mock_user.is_admin.return_value = False

    result = user_service.is_same_user_or_admin(mock_user,uuid.uuid4())

    assert result is False
