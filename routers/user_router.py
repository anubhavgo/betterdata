from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List

from schemas.user_schema import User,UserWithTokenResponse,UserLogin,UserBase,UserUpdate
from services.user_service import UserService
from sqlalchemy.orm import Session
from dependencies import get_db
from models.permission_model import *
from routers.utils import has_permission

router = APIRouter()

@router.post("", response_model=UserWithTokenResponse)
def create_user(user: User, db: Session = Depends(get_db)):
    user_service = UserService(db)
    new_user = user_service.create_user(user)
    return new_user

@router.get("/{user_id}", response_model=User)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db), requested_user=Depends(has_permission(DELETE_USER_PERMISSION))):
    user_service = UserService(db)
    deleted_user = user_service.delete_user(requested_user, user_id)
    if not deleted_user:
        raise HTTPException(status_code=400, detail="Bad Request. Unable to delete user")
    return {"message": "User deleted"}

@router.post("/login", response_model=UserWithTokenResponse)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.authenticate_user(user.username, user.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect Credentials. Unable to login")
    return user

@router.get("", response_model=List[User])
async def get_all_users(limit: int = 100, offset: int = 0, db: Session = Depends(get_db), requested_user=Depends(has_permission(GET_ALL_USERS_PERMISSION))):
    user_service = UserService(db)
    users = user_service.get_all_users(requested_user, limit, offset)
    return users

@router.put("/{user_id}", response_model=User)
def replace_user(user_id: str, user: UserBase, db: Session = Depends(get_db), requested_user=Depends(has_permission(UPDATE_USER_PERMISSION))):
    user_service = UserService(db)
    updated_user = user_service.replace_user(requested_user, user, user_id)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.patch("/{user_id}", response_model=User)
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db), requested_user=Depends(has_permission(UPDATE_USER_PERMISSION))):
    user_service = UserService(db)
    updated_user = user_service.update_user(requested_user, user, user_id)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user