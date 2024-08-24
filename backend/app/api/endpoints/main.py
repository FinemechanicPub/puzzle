from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import superuser
from app.schemas.menu import MenuBase, MenuResponse, MenuUpdateRequest
from app.repositories.menu import menu_repository
from app.core.db import get_async_session
from app.api.exceptions import MenuNotFoundException

router = APIRouter(prefix="/main", tags=["Main"])


@router.get("/menu/", response_model=list[MenuResponse])
async def list_menu(session: AsyncSession = Depends(get_async_session)):
    return await menu_repository.list(session)


@router.post(
    "/menu/",
    response_model=MenuResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(superuser)],
)
async def create_menu(
    menu_data: MenuBase,
    session: AsyncSession = Depends(get_async_session),
):
    return await menu_repository.create(session, menu_data)


@router.patch(
    "/menu/{menu_id}/",
    response_model=MenuResponse,
    dependencies=[Depends(superuser)],
)
async def update_menu(
    menu_id: int,
    menu_data: MenuUpdateRequest,
    session: AsyncSession = Depends(get_async_session),
):
    menu = await menu_repository.get(session, menu_id)
    if not menu:
        raise MenuNotFoundException
    return await menu_repository.update(session, menu, menu_data)


@router.delete(
    "/menu/{menu_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(superuser)],
)
async def delete_menu(
    menu_id: int, session: AsyncSession = Depends(get_async_session)
):
    menu = await menu_repository.get(session, menu_id)
    if not menu:
        raise MenuNotFoundException
    await menu_repository.remove(session, menu)
