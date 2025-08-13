from collections.abc import Callable
from typing import Annotated, TypeVar

from core.db import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .services import BaseService

Service = TypeVar('Service', bound=BaseService)


def get_service[Service](
        service_type: type[Service],
) -> Callable[[AsyncSession], Service]:
    """Create a FastAPI dependency for service injection using factory.
    """

    def _get_service(db: Annotated[AsyncSession, Depends(get_async_session)]) -> Service:
        return service_type(db_session=db)  # type: ignore

    return _get_service
