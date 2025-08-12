import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.base.models import BaseTimeStamp


class RefreshToken(BaseTimeStamp):
    """SQLAlchemy model representing a refresh token session.
    """

    __tablename__ = 'refresh_tokens'

    refresh_token: Mapped[uuid.UUID] = mapped_column(UUID, index=True)
    expires_in: Mapped[float]

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
    )
