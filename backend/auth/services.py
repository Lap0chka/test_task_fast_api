from sqlalchemy.ext.asyncio.session import AsyncSession

from .repository import UserRepository
from .schemas import CreateUserRequestSchema
from base.abstract import AbstractRepository
from base.services import BaseService


class UserService(BaseService):
    """Service for user."""
    def __init__(self, db_session: AsyncSession, repo: AbstractRepository=None):
        super().__init__(db_session)
        self.repo = repo or UserRepository()

    async def create_new_user(self, user: CreateUserRequestSchema) -> int:
        users_dict = user.model_dump()
        user_id = await self.repo.create_one(users_dict)
        return user_id
