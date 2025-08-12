from fastapi import FastAPI
from auth.router import router as auth_router
from core.db import engine, Base

app = FastAPI()

# (опционально) создать таблицы без Alembic при первом запуске:
# import asyncio
# async def _init():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
# asyncio.get_event_loop().run_until_complete(_init())

app.include_router(auth_router)