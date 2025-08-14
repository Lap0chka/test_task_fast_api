from typing import final

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from books.exceptions import ForgottenParametersException


class BaseService:
    """Base class for services."""

    def __init__(self, db_session: AsyncSession) -> None:
        """Initialize a new BaseService instance."""
        self._session: AsyncSession = db_session

    @property
    def session(self) -> AsyncSession:
        """Return the current AsyncSession."""
        return self._session

    @staticmethod
    @final
    def _validate_schema_for_update_request(
        schema: BaseModel,
    ) -> dict[str, str]:
        """Validate schema for update request"""
        
        schema_fields: dict[str, str] = schema.model_dump(
            exclude_none=True,
            exclude_unset=True,
        )
        if not schema_fields:
            raise ForgottenParametersException
        return schema_fields
