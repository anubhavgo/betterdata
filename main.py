from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uvicorn
from routers import user_router
from database import engine
from sqladmin import Admin
from sqladmin_utils import *
from middlewares.auth_filter import AuthMiddleware
# FastAPI app
app = FastAPI()

admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(PermissionAdmin)
admin.add_view(UserRoleAdmin)
admin.add_view(RolePermissionAdmin)

# Mount routers
app.include_router(
    user_router.router,
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)

auth_middleware = AuthMiddleware(app)

app.middleware("http")(auth_middleware)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)