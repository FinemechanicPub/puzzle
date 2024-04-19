from fastapi import APIRouter

from app.api.endpoints.game import game_router
from app.api.endpoints.piece import piece_router
from app.api.endpoints.play import play_router

main_router = APIRouter()
main_router.include_router(game_router, prefix='/games', tags=['Games'])
main_router.include_router(piece_router, prefix='/pieces', tags=['Pieces'])
main_router.include_router(play_router, prefix='/play', tags=['Games'])
