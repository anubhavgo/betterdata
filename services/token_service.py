from typing import List
from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from datetime import datetime, timedelta
from jose import JWTError, jwt
from schemas.user_schema import User
from schemas.token_schema import TokenData
import time
from fastapi import HTTPException

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class TokenService:
    def create_access_token(self,data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self,token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            exp = payload.get("exp")
            user_id = payload.get("user_id")
            if user_id is None or exp is None or exp < time.time():
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
            token_data = TokenData(user_id=user_id, exp=exp)
            return token_data
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")