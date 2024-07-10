from fastapi import APIRouter

from app.api.endpoints.cover import cover_router
from app.api.endpoints.game import game_router
from app.api.endpoints.piece import piece_router
from app.api.endpoints.play import play_router
from app.api.endpoints.user import user_router
from app.core.user import fastapi_users
from app.schemas.user import UserRead, UserUpdate

main_router = APIRouter()
main_router.include_router(cover_router, prefix='/cover', tags=['Main Page'])
main_router.include_router(game_router, prefix='/games', tags=['Games'])
main_router.include_router(piece_router, prefix='/pieces', tags=['Pieces'])
main_router.include_router(play_router, prefix='/play', tags=['Games'])
main_router.include_router(user_router, prefix='/auth', tags=['Authentication'])

main_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users", tags=["Users"],
)
