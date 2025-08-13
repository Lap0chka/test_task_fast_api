from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Table, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from core.db import Base

book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("author_id", ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("book_id", "author_id", name="uq_book_author"),
)

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    books: Mapped[List["Book"]] = relationship(
        back_populates="authors",
        secondary=book_authors,
        lazy="selectin",
    )

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    published_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    genres: Mapped[list[str]] = mapped_column(ARRAY(String(50)), nullable=False, server_default="{}")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    authors: Mapped[List[Author]] = relationship(
        back_populates="books",
        secondary=book_authors,
        lazy="selectin",
    )