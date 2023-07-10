from fastapi import FastAPI, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uvicorn
from routers import user_router,analytics_router
from database import engine
from sqladmin import Admin
from sqladmin_utils import *
from middlewares.auth_filter import AuthMiddleware
from middlewares.log_middleware import LoggingMiddleware
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

app.include_router(
    analytics_router.router,
    prefix="/analytics",
    tags=["Analytics"],
    responses={404: {"description": "Not found"}}
)

@app.get('/healthcheck', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    return {'healthcheck': 'Everything OK!'}

auth_middleware = AuthMiddleware(app)


app.middleware("http")(auth_middleware)
app.add_middleware(LoggingMiddleware)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)