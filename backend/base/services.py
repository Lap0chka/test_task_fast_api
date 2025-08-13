from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    """Base class for services."""

    def __init__(self, db_session: AsyncSession) -> None:
        """Initialize a new BaseService instance.
        """
        self._session: AsyncSession = db_session

    @property
    def session(self) -> AsyncSession:
        """Return the current AsyncSession."""
        return self._session
