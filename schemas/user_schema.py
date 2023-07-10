from typing import List, Optional
from pydantic import BaseModel,Extra
from schemas.address_schema import Address
from schemas.role_schema import Role
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    first_name: str
    last_name: str
    gender: str
    email: str
    phone: str
    birth_date: str
    avatar: str
    addresses: List[Address]
    status: str

class User(UserBase):
    id: Optional[UUID]
    username: str
    password: Optional[str]
    password_hash: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True
        fields = {'password': {'exclude':True}}

class UserWithTokenResponse(User):
    token: Optional[str]

class UserLogin(BaseModel):
    username: str
    password: str

class UserReplace(User):
    class Config:
        fields = {
            'password': {'exclude':True},
            'password_hash': {'exclude':True},
            'username': {'exclude':True},
            'created_at': {'exclude':True},
            'updated_at': {'exclude':True}
        }

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    birth_date: Optional[str]
    avatar: Optional[str]
    addresses: Optional[List[Address]]
    status: Optional[str]