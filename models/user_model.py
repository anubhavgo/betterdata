from sqlalchemy import Column, Integer, String, Table, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from database import Base
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(
        GUID,
        primary_key=True,
        index = True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    birth_date = Column(String)
    avatar = Column(String)
    addresses = Column(JSON)
    roles = relationship("Role", secondary="user_role", back_populates="users")
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    def is_admin(self):
        for role in self.roles:
            if role.id == "admin":
                return True
        return False