import datetime as dt
from typing import Any, TypeVar, cast, Sequence

from sqlalchemy import (
    Delete,
    Result,
    Select,
    Update,
    and_,
    desc,
    or_,
    select,
    update,
)
from sqlalchemy.sql.expression import insert

from base.abstract.repository import AbstractRepository
from core.db import Base, new_session

Model = TypeVar('Model', bound=Base)

class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def create_one(self, data: dict) -> Model:
        async with new_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_all(
            self,
            created_at: dt.datetime | None = None,
            last_id: int | None = None,
            limit: int | None = None,
            order_by: list[str] | None = None,
            *filters: Any,
            **filters_by: Any,
    ) -> list[Model] | None:
        async with new_session() as session:
            pagination = []
            if created_at and last_id:
                pagination = [
                    or_(
                        self.model.created_at < created_at,  # type: ignore
                        and_(
                            self.model.created_at == created_at,  # type: ignore
                            self.model.id < last_id,  # type: ignore
                        ),
                    )
                ]
            query: Select[Any] = (
                select(self.model)
                .where(*filters, *pagination)
                .filter_by(**filters_by)
            )
            if limit:
                query = query.limit(limit)
            result = await session.execute(query)
            return cast(list[Model], result.scalars().all())

    async def _get(self, *filters: Any, **filters_by: Any) -> Result[Any]:
        """Execute a database query with the specified filters.
        """
        async with new_session() as session:
            query: Select[Any] = (
                select(self.model).where(*filters).filter_by(**filters_by)
            )
            return await session.execute(query)

    async def get_one(self, *filters: Any, **filters_by: Any) -> Model | None:
        """Retrieve a single record matching the specified filters.
        """
        result: Result[Any] = await self._get(*filters, **filters_by)
        return result.scalar_one_or_none()

    async def update(
        self,
        update_data: dict[str, Any],
        *filters: Any,
        **filters_by: Any,
    ) -> Model | None:
        """Update records matching the specified filters with provided data.
        """
        async with new_session() as session:
            query: Update = (
                update(self.model)
                .where(*filters)
                .filter_by(**filters_by)
                .values(update_data)
                .returning(self.model)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def delete(
            self,
            *filters: Any,
            **filters_by: Any,
    ) -> None:
        """Delete records matching the specified filters.
        """
        async with new_session() as session:
            query: Delete = (
                Delete(self.model).where(*filters).filter_by(**filters_by)
            )
            await session.execute(query)

    async def get_ids_by_lst(self, lst: list[str]) -> list[model]:
        async with new_session() as session:
            res = await session.execute(
                select(self.model).where(self.model.name.in_(lst))
            )
            return list(res.scalars())

    async def add_many_to_many(
            self,
            obj: Model,
            rel_attr: str,
            items: Sequence[Model],
    ):
        async with new_session() as session:
            obj = await session.merge(obj)
            items_attached = [await session.merge(it) for it in items]

            rel_list = getattr(obj, rel_attr)
            existing = set(rel_list)
            for it in items_attached:
                if it not in existing:
                    rel_list.append(it)

            await session.commit()
            await session.refresh(obj)
            return obj


