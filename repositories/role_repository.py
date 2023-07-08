from sqlalchemy.orm import Session

from models.role_model import Role

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_role_by_id(self, id: str) -> Role:
        role = self.db.query(Role).filter(Role.id == id).first()
        return role