from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.auth.schemas import UserRegister, UserOut
from auth.controller import AuthController

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=201)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    controller = AuthController(db)
    return await controller.register(user_in)