from fastapi import status
from httpx import AsyncClient
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import superuser
from app.main import app
from app.models.menu import Menu
from app.models.user import User


SAMPLE_1 = {"title": "5x5", "query": {"height": 5, "width": 5}, "order": 1}
SAMPLE_2 = {"title": "6x6", "query": {"height": 6, "width": 6}, "order": 2}

SUPER_USER = User(is_active=True, is_superuser=True, is_verified=True)

CASES = [
    ["list_menu", "GET", {}, {}, status.HTTP_200_OK],
    ["create_menu", "POST", {}, SAMPLE_1, status.HTTP_401_UNAUTHORIZED],
    [
        "update_menu",
        "PATCH",
        {"menu_id": 1},
        SAMPLE_2,
        status.HTTP_401_UNAUTHORIZED,
    ],
    [
        "delete_menu",
        "DELETE",
        {"menu_id": 1},
        {},
        status.HTTP_401_UNAUTHORIZED,
    ],
]


@pytest.mark.parametrize("case", CASES)
async def test_menu_access(user_client: AsyncClient, case):
    endpoint, method, params, json, expected_status = case
    async with user_client as client:
        response = await client.request(
            method=method, url=app.url_path_for(endpoint, **params), json=json
        )
        assert response.status_code == expected_status


async def test_menu_read(session: AsyncSession, user_client: AsyncClient):
    session.add(Menu(**SAMPLE_2))
    await session.commit()
    async with user_client as client:
        response = await client.get(url=app.url_path_for("list_menu"))
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        menu_dict = data[0]
        del menu_dict["id"]
        assert menu_dict == SAMPLE_2


async def test_menu_create(session: AsyncSession, user_client: AsyncClient):
    async with user_client as client:
        app.dependency_overrides[superuser] = lambda: SUPER_USER
        response = await client.post(
            url=app.url_path_for("create_menu"), json=SAMPLE_1
        )
        del app.dependency_overrides[superuser]
        assert response.status_code == status.HTTP_201_CREATED
    menus = (await session.scalars(select(Menu))).all()
    assert len(menus) == 1
    menu = menus[0]
    assert menu.title == SAMPLE_1["title"]
    assert menu.order == SAMPLE_1["order"]
    assert menu.query == SAMPLE_1["query"]


async def test_menu_update(session: AsyncSession, user_client: AsyncClient):
    menu = Menu(**SAMPLE_2)
    session.add(menu)
    await session.commit()
    await session.refresh(menu)
    async with user_client as client:
        app.dependency_overrides[superuser] = lambda: SUPER_USER
        response = await client.patch(
            url=app.url_path_for("update_menu", menu_id=menu.id), json=SAMPLE_1
        )
        del app.dependency_overrides[superuser]
        assert response.status_code == status.HTTP_200_OK
    menus = (await session.scalars(select(Menu))).all()
    assert len(menus) == 1
    menu = menus[0]
    assert menu.title == SAMPLE_1["title"]
    assert menu.order == SAMPLE_1["order"]
    assert menu.query == SAMPLE_1["query"]


CASES_ORDER = [[SAMPLE_1, SAMPLE_2], [SAMPLE_2, SAMPLE_1]]


@pytest.mark.parametrize("menus", CASES_ORDER)
async def test_menu_order(session: AsyncSession, user_client: AsyncClient, menus):
    session.add_all(Menu(**menu) for menu in menus)
    await session.commit()

    async with user_client as client:
        response = await client.get(url=app.url_path_for("list_menu"))
        assert response.status_code == status.HTTP_200_OK
        menu_data = response.json()
        assert len(menu_data) == 2
        for menu, expected in zip(menu_data, (SAMPLE_1, SAMPLE_2)):
            del menu["id"]
            assert menu == expected
