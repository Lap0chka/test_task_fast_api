from typing import Any, TypeVar

from sqlalchemy import select, update, delete
from sqlalchemy.engine.result import Result
from sqlalchemy.sql.dml import Update, Delete
from sqlalchemy.sql.expression import insert
from sqlalchemy.sql.selectable import Select

from base.abstract.repository import AbstractRepository
from core.db import new_session, Base

Model = TypeVar('Model', bound=Base)

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

    async def _get(self, *filters: Any, **filters_by: Any) -> Result[Any]:
        """Execute a database query with the specified filters.
        """
        async with new_session() as session:
            query: Select[Any] = (
                select(self.model).where(*filters).filter_by(**filters_by)
            )
            return await session.execute(query)

    async def get_one(self, *filters: Any, **filters_by: Any) -> Model | None:
        """
        Retrieve a single record matching the specified filters.
        """

        result: Result[Any] = await self._get(*filters, **filters_by)
        return result.scalar_one_or_none()

    async def update(
        self,
        update_data: dict[str, Any],
        *filters: Any,
        **filters_by: Any,
    ) -> Model | None:
        """
        Update records matching the specified filters with provided data.
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
        """
        Delete records matching the specified filters.
        """
        async with new_session() as session:
            query: Delete = (
                Delete(self.model).where(*filters).filter_by(**filters_by)
            )
            await session.execute(query)
