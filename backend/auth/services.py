from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from users.models import User


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def is_username_taken(self, username: str) -> bool:
        stmt = select(User.id).where(func.lower(User.username) == username.lower())
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none() is not None

    async def create_user(self, username: str, password: str) -> User:
        user = User(username=username, password_hash="zdsadasdad12345")
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user