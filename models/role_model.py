from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    permissions = relationship("Permission", secondary="role_permission", back_populates="roles")
    users = relationship("User", secondary="user_role", back_populates="roles")