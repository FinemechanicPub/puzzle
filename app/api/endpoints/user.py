from fastapi import APIRouter

from app.core.user import fastapi_users, auth_backend

user_router = APIRouter()


# https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/auth/
user_router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth",
    tags=["auth"],
)
