from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy import (
    TIMESTAMP, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.base.models import BaseTimeStamp
from backend.core import Base

book_author = Table(
    "book_author",
    Base.metadata,
    Column("book_id", ForeignKey("book.id", ondelete="CASCADE"), primary_key=True),
    Column("author_id", ForeignKey("author.id", ondelete="CASCADE"), primary_key=True),
)

book_genre = Table(
    "book_genre",
    Base.metadata,
    Column("book_id", ForeignKey("book.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id", ondelete="CASCADE"), primary_key=True),
)


class Author(BaseTimeStamp):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(200), nullable=False, index=True, comment='Author name'
    )
    books: Mapped[List[Book]] = relationship(
        secondary=book_author,
        back_populates="authors",
        lazy="selectin",
    )


class Book(BaseTimeStamp):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(
        String(200), nullable=False, index=True, comment='Book name'
    )
    published_year = Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    authors: Mapped[List[Author]] = relationship(
        secondary=book_author,
        back_populates="books",
        lazy="selectin",
    )
    genres: Mapped[List["Genre"]] = relationship(
        secondary=book_genre,
        back_populates="books",
        lazy="selectin",
    )


class Genre(BaseTimeStamp):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    books: Mapped[List["Book"]] = relationship(
        secondary=book_genre,
        back_populates="genres",
        lazy="selectin",
    )
