from __future__ import annotations

from datetime import datetime
from typing import Literal, List

from pydantic import Field, field_validator
from pydantic import field_serializer

from base.schema import BaseSchema
from books.validators import clean_empty_values, clean_date
from core.settings import ALLOWED_GENRES


class BookBase(BaseSchema):
    title: str = Field(min_length=1, max_length=255)
    author_names: list[str] = Field(min_length=1)
    genres: list[Literal[*ALLOWED_GENRES]] = Field(min_length=1)
    published_year: int

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        return clean_empty_values(v)

    @field_validator("author_names")
    @classmethod
    def authors_non_empty(cls, v: list[str]) -> list[str]:
        clean_empty_values(v)
        return v

    @field_validator("published_year")
    @classmethod
    def year_range(cls, v: int) -> int:
        return clean_date(v)


class BookOutSchema(BaseSchema):
    id: int
    title: str
    authors: list[str]
    genres: list[str]
    published_year: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_serializer("authors")
    def serialize_authors(self, authors):
        return [a.name for a in authors]


class AuthorSchema(BaseSchema):
    name: str


class BulkUploadResult(BaseSchema):
    total: int
    created: int
    failed: int
    created_ids: List[int]
    errors: List[dict]
