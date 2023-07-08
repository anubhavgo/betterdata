from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(String, primary_key=True, index=True)
    description = Column(String)
    roles = relationship("Role", secondary="role_permission", back_populates="permissions")