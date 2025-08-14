from base.repository import SQLAlchemyRepository

from .models import AuthorModel, BookModel


class BookRepository(SQLAlchemyRepository):
    model = BookModel


class AuthorRepository(SQLAlchemyRepository):
    model = AuthorModel
