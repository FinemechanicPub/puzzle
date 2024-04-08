from app.crud.base import CRUDBase
from app.models.game import Game


class CRUDGame(CRUDBase):
    pass


game_crud = CRUDGame(Game)
