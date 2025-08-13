from typing import Type, Any

from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound

from base.abstract.repository import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def get_one(self, id: int) -> dict:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if not obj:
            raise NoResultFound(f"{self.model.__name__} with id={id} not found")
        return obj.__dict__

    async def create_one(self, data: dict) -> int:
        async with async_session_maker()

    async def update_one(self, id: int, data: dict) -> dict:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if not obj:
            raise NoResultFound(f"{self.model.__name__} with id={id} not found")
        await self.session.commit()
        return obj.__dict__

    async def delete_one(self, id: int) -> dict:
        stmt = (
            delete(self.model)
            .where(self.model.id == id)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if not obj:
            raise NoResultFound(f"{self.model.__name__} with id={id} not found")
        await self.session.commit()
        return obj.__dict__

    async def get_all_or_by_filter(self, **kwargs) -> list[dict]:
        p
