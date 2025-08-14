import logging

from auth.router import auth_router
from books.routers import author_router, book_router
from core.db import lifespan
from fastapi import FastAPI

logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(book_router)
app.include_router(author_router)
