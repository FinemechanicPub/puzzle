from fastapi import APIRouter

from app.schemas.board import Board


router = APIRouter()


@router.get('/board')
def board() -> Board:
    return Board(width=5, height=5)
