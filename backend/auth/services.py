import uuid
from typing import cast

from base.abstract import AbstractRepository
from base.services import BaseService
from sqlalchemy.ext.asyncio.session import AsyncSession

from .exceptions import (
    RefreshTokenException,
    UserNotFoundByIdException,
    WrongCredentialsException,
)
from .models import RefreshTokenModel, UserModel
from .repository import AuthRepository, UserRepository
from .schemas import CreateRefreshTokenSchema, CreateUserRequestSchema, Token
from .secure import Hasher
from .token import TokenManager


class UserService(BaseService):
    """Service for user."""

    def __init__(self, db_session: AsyncSession, repo: AbstractRepository = None):
        super().__init__(db_session)
        self.repo = repo or UserRepository()

    async def create_new_user(self, user: CreateUserRequestSchema) -> int:
        users_dict = user.model_dump()
        users_dict["password"] = Hasher.hash_password(users_dict["password"])
        return await self.repo.create_one(users_dict)

    async def get_user_by_id(self, user_id: int) -> UserModel:
        """Retrieve a user by their ID from the database."""
        async with self.session.begin():
            user: UserModel | None = await self.repo.get_one(id=user_id)
        if not user:
            raise UserNotFoundByIdException
        return user


class AuthService(BaseService):
    def __init__(self, db_session: AsyncSession, repo: AbstractRepository = None):
        super().__init__(db_session)
        self.repo = repo or AuthRepository()
        self.user_repo = UserRepository()

    def auth_repo(self) -> AuthRepository:
        """Return the AuthDAO instance."""
        return self.repo

    @staticmethod
    def _verify_user_password(user: UserModel | None, password: str) -> None:
        """Verify that the given password matches the user's password."""
        if not user or not Hasher.verify_password(password, user.password):
            raise WrongCredentialsException

    async def auth_user(self, username: str, password: str) -> UserModel:
        """Authenticate a user by email and password."""
        user: UserModel | None = await self.user_repo.get_one(
            username=username, is_active=True
        )
        self._verify_user_password(user, password)
        return cast(UserModel, user)

    @staticmethod
    def _get_user_id_from_jwt(decoded_jwt: dict[str, str | int]) -> str:
        """Extract and return user ID from a decoded JWT payload."""
        user_id: int | str | None = decoded_jwt.get("sub")
        if not user_id or isinstance(user_id, int):
            raise WrongCredentialsException
        return user_id

    async def validate_token_for_user(self, user_jwt_token: str) -> int:
        """Validate a JWT token and retrieve the associated user.

        This method decodes the provided JWT token, validates its expiration,
        and retrieves the associated user from the database.
        """
        decoded_jwt: dict[str, str | int] = TokenManager.decode_access_token(
            token=user_jwt_token,
        )
        TokenManager.validate_access_token_expired(decoded_jwt)
        user_id: uuid.UUID | str = self._get_user_id_from_jwt(decoded_jwt)
        if not user_id:
            raise WrongCredentialsException
        return user_id

    async def create_token(self, user_id: int) -> Token:
        """Generate new access and refresh tokens for a user.

        This method creates a new pair of tokens (access and refresh)
        for the given user,
        deletes any existing refresh tokens for that user,
         and stores the new refresh token
        in the database.


        """
        access_token: str = TokenManager.generate_access_token(user_id=user_id)
        refresh_token, tm_delta = TokenManager.generate_refresh_token()
        create_token_schema = CreateRefreshTokenSchema(
            user_id=user_id,
            refresh_token=refresh_token,
            expires_in=tm_delta.total_seconds(),
        )

        await self.repo.delete(RefreshTokenModel.user_id == user_id)
        await self.repo.create_one(create_token_schema.model_dump())
        return Token(
            access_token=access_token,
            refresh_token=str(refresh_token),
        )

    async def refresh_token(self, refresh_token: uuid.UUID) -> Token:
        """Generate new access and refresh tokens.
        This method validates the provided refresh token, checks
         if it exists and hasn't expired,
        then generates new access and refresh tokens for the user.
        """
        refresh_token_model: RefreshTokenModel | None = await self.repo.get_one(
            refresh_token=refresh_token,
        )
        if not refresh_token_model:
            raise RefreshTokenException
        TokenManager.validate_refresh_token_expired(
            refresh_token_model=refresh_token_model,
        )
        user_id: uuid.UUID = refresh_token_model.user_id
        user: UserModel | None = await self.repo.get_one(
            id=user_id,
        )
        if not user:
            raise RefreshTokenException
        access_token: str = TokenManager.generate_access_token(
            user_id=user_id,
        )
        updated_refresh_token, tm_delta = TokenManager.generate_refresh_token()
        updated_refresh_token_model: RefreshTokenModel | None = await self.repo.update(
            {
                "refresh_token": updated_refresh_token,
                "expires_in": tm_delta.total_seconds(),
            },
            id=refresh_token_model.id,
        )
        if not updated_refresh_token_model:
            raise RefreshTokenException
        return Token(
            access_token=access_token,
            refresh_token=str(updated_refresh_token),
        )

    async def logout_user(
        self,
        refresh_token: str | None,
    ) -> None:
        """Log out a user by invalidating their refresh token."""
        if not refresh_token:
            raise RefreshTokenException
        refresh_token_model: RefreshTokenModel | None = await self.repo.get_one(
            refresh_token=refresh_token,
        )
        if not refresh_token_model:
            raise RefreshTokenException
        await self.repo.delete(
            id=refresh_token_model.id,
        )
