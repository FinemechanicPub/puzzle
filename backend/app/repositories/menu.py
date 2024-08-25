from app.models.menu import Menu
from app.repositories.repository import RepositoryBase


class MenuRepository(RepositoryBase[Menu]):
    order_by = "order"


menu_repository = MenuRepository(Menu)
