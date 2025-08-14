import uuid
from typing import Annotated

from base.dependencies import get_service
from core.settings import API_URL, MAX_AGE_ACCESS_TOKEN, MAX_AGE_REFRESH_TOKEN
from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from auth.exceptions import RefreshTokenException
from auth.models import UserModel
from auth.schemas import CreateUserRequestSchema, Token, UserResponseSchema
from auth.services import AuthService, UserService

auth_router = APIRouter(prefix=f"{API_URL}/auth", tags=["auth"])


@auth_router.post(
    "/register",
    description="Create a new user",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_schema: CreateUserRequestSchema,
    service: Annotated[UserService, Depends(get_service(UserService))],
) -> UserResponseSchema:
    """Endpoint to create a new user."""
    new_user = await service.create_new_user(user=user_schema)
    return UserResponseSchema.model_validate(new_user)


@auth_router.post(path="/login", response_model=Token)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends(get_service(AuthService))],
    response: Response,
) -> Token:
    """Authenticate user and issue JWT access and refresh tokens."""
    user: UserModel = await service.auth_user(
        username=form_data.username,
        password=form_data.password,
    )
    token: Token = await service.create_token(user.id)
    response.set_cookie(
        "access_token",
        token.access_token,
        max_age=MAX_AGE_ACCESS_TOKEN,
        httponly=True,
    )
    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        max_age=MAX_AGE_REFRESH_TOKEN,
        httponly=True,
    )
    return token


@auth_router.post(path="/refresh", response_model=Token)
async def refresh_token(
    request: Request,
    response: Response,
    service: Annotated[AuthService, Depends(get_service(AuthService))],
) -> Token:
    """Refresh the access and refresh tokens."""
    token: Token = await service.refresh_token(
        refresh_token=uuid.UUID(request.cookies.get("refresh_token")),
    )
    response.set_cookie(
        "access_token",
        token.access_token,
        max_age=MAX_AGE_ACCESS_TOKEN,
        httponly=True,
    )
    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        max_age=MAX_AGE_REFRESH_TOKEN,
        httponly=True,
    )
    return token


@auth_router.delete(path="/logout", response_model=dict[str, str])
async def logout_user(
    request: Request,
    response: Response,
    service: Annotated[AuthService, Depends(get_service(AuthService))],
) -> dict[str, str]:
    """Log out the user."""
    raw_token = request.cookies.get("refresh_token")
    if not raw_token:
        raise RefreshTokenException

    await service.logout_user(str(raw_token))
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}
