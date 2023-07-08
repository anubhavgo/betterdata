from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List

from schemas.user_schema import User,UserWithTokenResponse,UserLogin,UserBase
from services.user_service import UserService
from sqlalchemy.orm import Session
from dependencies import get_db

router = APIRouter()

async def validate_auth_role(request: Request, user_id: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if user is None or not (user.is_admin() or (user_id == request.state.user_id)):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

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
def delete_user(request: Request, user_id: str, db: Session = Depends(get_db),login_user=Depends(validate_auth_role)):
    user_service = UserService(db)
    user = user_service.delete_user(user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Bad Request")
    return {"message": "User deleted"}

@router.post("/login", response_model=UserWithTokenResponse)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.authenticate_user(user.username, user.password)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

@router.put("/{user_id}", response_model=User)
def replace_user(request: Request, user_id: str, user: UserBase, db: Session = Depends(get_db),login_user=Depends(validate_auth_role)):
    user_service = UserService(db)
    updated_user = user_service.replace_user(user_id, user)
    print(updated_user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# @router.patch("/{user_id}", response_model=user_schema.User)
# def update_user(request: Request, user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
#     user_service = UserService(db)
#     updated_user = user_service.update_user(request.state.user_id, user_id, user)
#     if not updated_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return updated_user

# @router.get("/", response_model=List[user_schema.User])
# def get_all_users(db: Session = Depends(get_db)):
#     user_service = UserService(db)
#     users = user_service.get_all_users()
#     return users

