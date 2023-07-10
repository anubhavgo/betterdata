from typing import List
from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from services.token_service import TokenService
from schemas.user_schema import User,UserWithTokenResponse,UserBase
from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

TOKEN_EXPIRE_TIME_FOR_LOGIN = 1440  # 24 hours

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.token_service = TokenService()

    def create_user(self, user: User):
        try:
            user.password_hash = self.user_repo.get_password_hash(user.password)
            new_user = self.user_repo.create_user(user)
            data = {"user_id": str(new_user.id), "email": new_user.email}
            access_token = self.token_service.create_access_token(data=data, expires_delta=timedelta(minutes=TOKEN_EXPIRE_TIME_FOR_LOGIN))
            new_user = UserWithTokenResponse.from_orm(new_user)
            new_user.token = access_token
            return new_user
        except IntegrityError as ex:
            raise HTTPException(status_code=400, detail=str(ex.orig.diag.message_detail))

    def get_all_users(self, requested_user, limit=None, offset=None):
        if not requested_user.is_admin():
            raise HTTPException(status_code=401, detail="Does not have permission to fetch users")
        users = self.user_repo.get_all_users(offset, limit)
        return users

    def get_user(self, user_id: str):
        user = self.user_repo.get_user_by_id(user_id)
        return user
    
    def replace_user(self, requested_user, user_update: UserBase, user_id: str):
        if not self.is_same_user_or_admin(requested_user, user_id):
            raise HTTPException(status_code=401, detail="Does not have permission to replace user")
        updated_user = self.user_repo.replace_user(user_update, user_id)
        return updated_user
    
    def update_user(self, requested_user, user_update: UserBase, user_id: str):
        if not self.is_same_user_or_admin(requested_user, user_id):
            raise HTTPException(status_code=401, detail="Does not have permission to update user attributes")
        updated_user = self.user_repo.update_user(user_update, user_id)
        return updated_user
    
    def update_user_attributes(self, user_id: str, user_update: UserBase):
        user = self.get_user(user_id)
        if not user: return
        updated_data = user_update.dict(exclude_unset=True)
        for field, value in updated_data.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, requested_user, user_id: str):
        if not self.is_same_user_or_admin(requested_user, user_id):
            raise HTTPException(status_code=401, detail="Does not have permission to delete user")
        return self.user_repo.delete_user(user_id)

    def authenticate_user(self, username: str, password: str):
        user = self.user_repo.get_user_by_username(username)
        if not user or not self.user_repo.verify_password(password, user.password_hash):
            return None
        data = {"user_id": str(user.id), "email": user.email}
        access_token = self.token_service.create_access_token(data=data, expires_delta=timedelta(minutes=TOKEN_EXPIRE_TIME_FOR_LOGIN))
        new_user = UserWithTokenResponse.from_orm(user)
        new_user.token = access_token
        return new_user
    
    def is_same_user_or_admin(self, user, user_id: str):
        if user.is_admin() or str(user.id) == user_id:
            return True
        return False