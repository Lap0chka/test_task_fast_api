from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import Field, field_validator

from base.schema import BaseSchema

ALLOWED_GENRES = ("Fiction", "Non-Fiction", "Science", "Fantasy", "History", "Biography")


class BookBase(BaseSchema):
    title: str = Field(min_length=1, max_length=255)
    author_names: list[str] = Field(min_length=1)  # список имён авторов
    genres: list[Literal[*ALLOWED_GENRES]] = Field(min_length=1)
    published_year: int

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("title must be a non-empty string")
        return v

    @field_validator("author_names")
    @classmethod
    def authors_non_empty(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("author_names must be a non-empty list")
        cleaned = [name.strip() for name in v]
        if any(not name for name in cleaned):
            raise ValueError("each author name must be a non-empty string")
        # убираем дубликаты, сохраняя порядок
        dedup: list[str] = []
        for name in cleaned:
            if name not in dedup:
                dedup.append(name)
        return dedup

    @field_validator("published_year")
    @classmethod
    def year_range(cls, v: int) -> int:
        from datetime import datetime
        current_year = datetime.utcnow().year
        if v < 1800 or v > current_year:
            raise ValueError(f"published_year must be between 1800 and {current_year}")
        return v


class BookUpdate(BaseSchema):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    author_names: Optional[list[str]] = None
    genres: Optional[list[Literal[*ALLOWED_GENRES]]] = None
    published_year: Optional[int] = None

    @field_validator("title")
    @classmethod
    def title_not_blank_opt(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("title must be a non-empty string")
        return v

    @field_validator("author_names")
    @classmethod
    def authors_non_empty_opt(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is None:
            return v
        if not v:
            raise ValueError("author_names must be a non-empty list")
        cleaned = [name.strip() for name in v]
        if any(not name for name in cleaned):
            raise ValueError("each author name must be a non-empty string")
        dedup: list[str] = []
        for name in cleaned:
            if name not in dedup:
                dedup.append(name)
        return dedup

    @field_validator("published_year")
    @classmethod
    def year_range_opt(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return v
        from datetime import datetime
        current_year = datetime.utcnow().year
        if v < 1800 or v > current_year:
            raise ValueError(f"published_year must be between 1800 and {current_year}")
        return v

class BookOut(BaseSchema):
    id: int
    title: str
    authors: list[str]
    genres: list[str]
    published_year: int
    created_at: datetime | None = None
    updated_at: datetime | None = None