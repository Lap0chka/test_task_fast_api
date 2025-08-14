import uuid

from base.schema import BaseSchema
from pydantic import Field


class CreateUserRequestSchema(BaseSchema):
    """Pydantic model for create user."""

    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)


class UserResponseSchema(BaseSchema):
    """Pydantic model for user response."""

    id: int = Field()
    username: str = Field(min_length=3, max_length=64)


class Token(BaseSchema):
    """Pydantic model for token."""

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"  # noqa: S105


class CreateRefreshTokenSchema(BaseSchema):
    """Pydantic model for creating a new refresh token session.

    This schema defines the structure for creating a new refresh token session
    in the database. It includes the user ID, refresh token value.
    """

    user_id: int
    refresh_token: uuid.UUID
    expires_in: float
