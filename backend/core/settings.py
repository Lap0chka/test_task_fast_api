import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv("DEBUG")

# JWT
SECRET_KEY: str = os.getenv("SECRET_KEY_JWT")
ALGORITHM: str = os.getenv("ALGORITHM_JWT")
ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
REFRESH_TOKEN_EXPIRE_DAYS: int = 30
MAX_AGE_TOKEN = ACCESS_TOKEN_EXPIRE_MINUTES * 60
MAX_AGE_REFRESH_TOKEN = REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60
