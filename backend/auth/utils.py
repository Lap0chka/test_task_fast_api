import logging
from passlib.context import CryptContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a plain text password using the configured CryptContext.
    """
    if not password:
        logger.error("Attempted to hash an empty password.")
        raise ValueError("Password cannot be empty.")

    return pwd_context.hash(password)