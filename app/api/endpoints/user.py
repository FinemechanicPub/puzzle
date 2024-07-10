from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.authentication import Strategy

from app.api.exceptions import BadCredentialsException, UserNotVerifiedException
from app.core.config import settings
from app.core.user import UserManager, auth_backend, get_user_manager, user_token
from app.schemas.user import LoginRequest

user_router = APIRouter()


# # https://fastapi-users.github.io/fastapi-users/latest/configuration/routers/auth/
# user_router.include_router(
#     fastapi_users.get_auth_router(auth_backend, requires_verification=True),
#     prefix="/auth",
#     tags=["auth"],
# )


@user_router.post('/login')
async def login(
    login_details: LoginRequest,
    request: Request,
    user_manager: UserManager = Depends(get_user_manager),
    strategy: Strategy = Depends(auth_backend.get_strategy),
):
    user = await user_manager.authenticate(
        OAuth2PasswordRequestForm(
            username=login_details.email, password=login_details.password
        )
    )
    if user is None or not user.is_active:
        raise BadCredentialsException
    if not settings.unverified_user_can_login and not user.is_verified:
        raise UserNotVerifiedException
    response = await auth_backend.login(strategy, user)
    await user_manager.on_after_login(user, request, response)
    return response


@user_router.post('/logout',)
async def logout(
    user_token: tuple = Depends(user_token),
    strategy: Strategy = Depends(auth_backend.get_strategy),
):
    user, token = user_token
    return await auth_backend.logout(strategy, user, token)
