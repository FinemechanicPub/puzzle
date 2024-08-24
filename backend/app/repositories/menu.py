from app.models.menu import Menu
from app.repositories.repository import RepositoryBase


class MenuRepository(RepositoryBase[Menu]):
    pass


menu_repository = MenuRepository(Menu)
