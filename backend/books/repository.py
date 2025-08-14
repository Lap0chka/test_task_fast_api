from base.repository import SQLAlchemyRepository
from .models import BookModel, AuthorModel


class BookRepository(SQLAlchemyRepository):
    model = BookModel


class AuthorRepository(SQLAlchemyRepository):
    model = AuthorModel


