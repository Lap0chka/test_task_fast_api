from datetime import datetime

from core.db import Base
from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column


class BaseUUIDModel(Base):
    """Base model for a UUID primary key."""

    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


class BaseTimeStampModel(BaseUUIDModel):
    """Base model for timestamp fields."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
