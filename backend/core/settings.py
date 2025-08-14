import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False


# JWT
SECRET_KEY: str = os.getenv("SECRET_KEY_JWT")
ALGORITHM: str = os.getenv("ALGORITHM_JWT")
ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
REFRESH_TOKEN_EXPIRE_DAYS: int = 30
MAX_AGE_ACCESS_TOKEN = ACCESS_TOKEN_EXPIRE_MINUTES * 60
MAX_AGE_REFRESH_TOKEN = REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60

# Api Version
API_VERSION = 'v1'
API_URL = f'/api/{API_VERSION}'

# Postgres config
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "books_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

ASYNC_DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


ALLOWED_GENRES = ("Fiction", "Non-Fiction", "Science", "Fantasy", "History", "Biography")