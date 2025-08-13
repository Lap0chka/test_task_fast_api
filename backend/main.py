import logging

from auth.router import auth_router
from core.db import lifespan
from fastapi import FastAPI

logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
