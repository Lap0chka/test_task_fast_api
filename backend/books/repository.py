from sqlalchemy import (
    select,
)

from base.repository import SQLAlchemyRepository
from books.models import BookModel, AuthorModel
from core.db import new_session


class BookRepository(SQLAlchemyRepository):
    model = BookModel


class AuthorRepository(SQLAlchemyRepository):
    model = AuthorModel


