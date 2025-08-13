from pydantic import Field

from base.schema import BaseSchema


class CreateUserRequestSchema(BaseSchema):
    """Pydantic model for create user."""
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)
