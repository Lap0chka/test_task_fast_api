from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql.expression import insert

from base.abstract.repository import AbstractRepository
from core.db import new_session


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def create_one(self, data: dict) -> int:
        async with new_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_all_or_by_filter(self, **filtered_by) -> list[dict]:
        async with new_session() as session:
            stmt = select(self.model).where(*filtered_by)
            instance = await session.execute(stmt)
            res = [row[0].to_read_model() for row in instance.all()]
            return res

    async def get_one(self, id: int) -> dict:
        async with new_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            if obj is None:
                raise NoResultFound(f"{self.model.__name__} id={id} not found")
            return obj.to_read_model()

    async def update_one(self, id: int, data: dict) -> dict:
        async with new_session() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**data)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            if obj is None:
                raise NoResultFound(f"{self.model.__name__} id={id} not found")
            await session.commit()
            return obj.to_read_model()

    async def delete_one(self, id: int) -> dict:
        async with new_session() as session:
            stmt = (
                delete(self.model)
                .where(self.model.id == id)
                .returning(self.model)
            )
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            if obj is None:
                raise NoResultFound(f"{self.model.__name__} id={id} not found")
            await session.commit()
            return obj.to_read_model()
