from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one(self, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, id: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, data: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> int:
        raise NotImplementedError

    async def get_all_or_by_filter(self, **kwargs) -> list[dict]:
        raise NotImplementedError




