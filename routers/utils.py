from fastapi import HTTPException, Depends, Request
from services.user_service import UserService
from sqlalchemy.orm import Session
from dependencies import get_db

def has_permission(permission: str):
    def _has_permission(request: Request, db: Session = Depends(get_db)):
        user_service = UserService(db)
        user = user_service.get_user(request.state.user_id)
        if user is None or not user.has_permission(permission):
            raise HTTPException(status_code=401, detail="Unauthorized, User does not have permission for {}".format(permission))
        return user
    return _has_permission