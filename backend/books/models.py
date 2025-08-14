from __future__ import annotations

from base.models import BaseTimeStampModel
from core.db import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("author_id", ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("book_id", "author_id", name="uq_book_author"),
)


class AuthorModel(BaseTimeStampModel):
    __tablename__ = "authors"
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )

    books: Mapped[list[BookModel]] = relationship(
        back_populates="authors",
        secondary=book_authors,
        lazy="selectin",
    )


class BookModel(BaseTimeStampModel):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    published_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    genres: Mapped[list[str]] = mapped_column(
        ARRAY(String(50)), nullable=False, server_default="{}"
    )

    authors: Mapped[list[AuthorModel]] = relationship(
        back_populates="books",
        secondary=book_authors,
        lazy="selectin",
    )
