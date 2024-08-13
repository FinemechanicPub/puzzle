from fastapi import APIRouter

from app.api.endpoints.cover import router as cover_router
from app.api.endpoints.game import router as game_router
from app.api.endpoints.piece import router as piece_router
from app.api.endpoints.play import router as play_router
from app.api.endpoints.user import router as user_router
from app.core.user import fastapi_users
from app.schemas.user import UserRead, UserUpdate

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(cover_router)
main_router.include_router(game_router)
main_router.include_router(piece_router)
main_router.include_router(play_router)
main_router.include_router(user_router)

main_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)
