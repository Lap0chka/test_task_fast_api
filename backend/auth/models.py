import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from base.models import BaseTimeStampModel


class UserModel(BaseTimeStampModel):
    """
    SQLAlchemy model representing a user in the system.
    """

    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
    )



class RefreshTokenModel(BaseTimeStampModel):
    """
    SQLAlchemy model representing a refresh token session.
    """

    __tablename__ = 'refresh_tokens'

    refresh_token: Mapped[uuid.UUID] = mapped_column(UUID, index=True)
    expires_in: Mapped[float]

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
    )
