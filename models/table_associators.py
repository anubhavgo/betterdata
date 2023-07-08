from sqlalchemy import Column, Integer, String, Table, ForeignKey, JSON,UniqueConstraint

from database import Base
from models.user_model import User
from models.role_model import Role
from models.permission_model import Permission
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(
        GUID,
        primary_key=True,
        index = True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    user_id = Column('user_id', GUID, ForeignKey(User.id))
    role_id = Column('role_id', String, ForeignKey(Role.id))
    __table_args__ = (UniqueConstraint('user_id', 'role_id'),)

class RolePermission(Base):
    __tablename__ = "role_permission"

    id = Column(
        GUID,
        primary_key=True,
        index = True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    role_id = Column('role_id', String, ForeignKey(Role.id))    
    permission_id = Column('permission_id', String, ForeignKey(Permission.id))
    __table_args__ = (UniqueConstraint('role_id', 'permission_id'),)