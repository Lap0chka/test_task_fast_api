from typing import final

from pydantic import BaseModel, ConfigDict

from books.exceptions import ForgottenParametersException


class BaseSchema(BaseModel):
    """Base Pydantic model for all schemas."""

    model_config = ConfigDict(from_attributes=True)


class DeleteResponse(BaseModel):
    status: str


