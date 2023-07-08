from sqladmin import Admin, ModelView
from models.user_model import User
from models.role_model import Role
from models.permission_model import Permission
from models.table_associators import UserRole, RolePermission


class UserAdmin(ModelView, model=User):
    column_list = [
                User.id, 
                User.first_name,
                User.last_name,
                User.gender,
                User.email,
                User.phone,
                User.username,
                User.password_hash,
                User.birth_date,
                User.avatar,
                User.addresses,
                User.roles,
                User.status,
                User.created_at,
                User.updated_at
    ]

class RoleAdmin(ModelView, model=Role):
    column_list = [
        Role.id,
        Role.name,
        Role.permissions,
        Role.users
    ]

class PermissionAdmin(ModelView, model=Permission):
    column_list = [
        Permission.id,
        Permission.description,
        Permission.roles
    ]

class UserRoleAdmin(ModelView, model=UserRole):
    column_list = [
        UserRole.id,
        UserRole.user_id,
        UserRole.role_id
    ]

class RolePermissionAdmin(ModelView, model=RolePermission):
    column_list = [
        RolePermission.id,
        RolePermission.permission_id,
        RolePermission.role_id
    ]