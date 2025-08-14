from typing import final

from books.exceptions import ForgottenParametersException
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base Pydantic model for all schemas."""

    model_config = ConfigDict(from_attributes=True)


class DeleteResponse(BaseModel):
    status: str
