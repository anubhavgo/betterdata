from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import update

from models.user_model import User
from models.role_model import Role
from models.permission_model import Permission
from uuid import UUID
from repositories.role_repository import RoleRepository
from passlib.context import CryptContext

DEFAULT_USER_ROLE = "customer"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        self.role_repo = RoleRepository(db)

    def get_all_users(self):
        users = self.db.query(User).all()
        return users

    def get_user_by_id(self, user_id: str):
        try:
            user = self.db.query(User).filter(User.id == UUID(user_id)).first()
            return user
        except ValueError:
            return None
        
    def get_user_by_username(self, username: str):
        try:
            user = self.db.query(User).filter(User.username == username).first()
            return user
        except ValueError:
            return None
            
    def create_user(self, user: User):
        new_user = User(**user.dict())
        self.db.add(new_user)
        customer_role = self.role_repo.get_role_by_id(DEFAULT_USER_ROLE)
        new_user.roles.append(customer_role)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, user_id: str, updated_user: User):
        user = self.get_user_by_id(user_id)
        if not user: return
        for field, value in updated_user.dict().items():
            setattr(user, field, value)
        self.db.commit()
        print(user)
        return user

    def delete_user(self, user_id: str):
        user = self.get_user_by_id(user_id)
        if not user:
            return user
        self.db.delete(user)
        self.db.commit()
        return user
    
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)