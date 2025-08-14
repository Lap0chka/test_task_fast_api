from __future__ import annotations

from typing import List

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base.models import BaseTimeStampModel
from core.db import Base


class BookAuthor(Base):
    """
    Association object between books and authors.
    """
    __tablename__ = "book_authors"
    __table_args__ = (UniqueConstraint("book_id", "author_id", name="uq_book_author"),)

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"),
                                         primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"),
                                           primary_key=True)

    book: Mapped["BookModel"] = relationship(back_populates="book_authors")
    author: Mapped["AuthorModel"] = relationship(back_populates="author_books")



class AuthorModel(BaseTimeStampModel):
    __tablename__ = "authors"
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )

    books: Mapped[List[BookAuthor]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class BookModel(BaseTimeStampModel):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    published_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    genres: Mapped[list[str]] = mapped_column(
        ARRAY(String(50)), nullable=False, server_default="{}"
    )

    authors: Mapped[List[BookAuthor]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
