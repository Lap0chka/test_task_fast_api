from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.engine.result import Result


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one(self, data: dict) -> int:
        raise NotImplementedError

    async def _get(self, *filters: Any, **filters_by: Any) -> Result[Any]:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, *filters: Any, **filters_by: Any) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, data: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> int:
        raise NotImplementedError

    async def get_all_or_by_filter(self, **kwargs) -> list[dict]:
        raise NotImplementedError




