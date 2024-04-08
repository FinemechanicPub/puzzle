from fastapi import APIRouter

from app.api.endpoints.game import game_router

main_router = APIRouter()
main_router.include_router(game_router, prefix='/games', tags=['Games'])
