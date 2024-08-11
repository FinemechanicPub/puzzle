import logging
from typing import Any, Dict, Optional

from fastapi import Depends, Request, Response
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User, AccessToken

logger = logging.getLogger(__name__)


# https://fastapi-users.github.io/fastapi-users/latest/configuration/user-manager/
class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        logger.info(
            "User '%s' has registered under id %d", user.email, user.id
        )

    async def on_after_update(
        self,
        user: User,
        update_dict: Dict[str, Any],
        request: Optional[Request] = None,
    ):
        for field, value in update_dict.items():
            if field == "password":
                value = "****"
            logger.info(
                "User #%d has updated field '%s' to '%s'",
                user.id,
                field,
                value,
            )

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        await self.user_db.update(user, dict())
        logger.info("User #%d has logged in", user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info("User #%d has forgot their password.", user.id)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info("Verification requested for user #%d.", user.id)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
):
    yield UserManager(user_db)


# https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/strategies/database/
async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


# https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/strategies/database/
def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(
        get_access_token_db
    ),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


cookie_transport = CookieTransport(cookie_name="puzzleuserauth")

auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

user_token = fastapi_users.authenticator.current_user_token(
    active=True, verified=False
)
try_verified_user = fastapi_users.current_user(True, True, True)
verified_user = fastapi_users.current_user(active=True, verified=True)
superuser = fastapi_users.current_user(active=True, superuser=True)
