from sqlalchemy.ext.asyncio.session import AsyncSession

from .repository import UserRepository
from .schemas import CreateUserRequestSchema
from base.abstract import AbstractRepository
from base.services import BaseService
from .utils import hash_password


class UserService(BaseService):
    """Service for user."""
    def __init__(self, db_session: AsyncSession, repo: AbstractRepository=None):
        super().__init__(db_session)
        self.repo = repo or UserRepository()

    async def create_new_user(self, user: CreateUserRequestSchema) -> int:
        users_dict = user.model_dump()
        users_dict["password"] = hash_password(users_dict["password"])
        return await self.repo.create_one(users_dict)
