from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.schemas import UserRegister, UserOut
from app.auth.service import AuthService

class AuthController:
    def __init__(self, db: AsyncSession):
        self.service = AuthService(db)

    async def register(self, user_in: UserRegister) -> UserOut:
        if await self.service.is_username_taken(user_in.username):
            raise HTTPException(status_code=400, detail="Username already exists")
        user = await self.service.create_user(user_in.username, user_in.password)
        return UserOut(id=user.id, username=user.username)