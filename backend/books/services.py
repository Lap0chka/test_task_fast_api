import datetime as dt

from sqlalchemy.ext.asyncio.session import AsyncSession

from base.abstract import AbstractRepository
from base.services import BaseService
from books.exceptions import AuthorNotExistException, BookNotFoundByIdException
from books.models import BookModel, AuthorModel
from books.repository import BookRepository, AuthorRepository
from books.schemas import BookBase, AuthorSchema


class BookService(BaseService):
    """Service class for handling course-related business logic."""

    def __init__(self, db_session: AsyncSession, repo: AbstractRepository = None):
        super().__init__(db_session)
        self.repo = repo or BookRepository()
        self.author_repo = AuthorRepository()

    async def create_book(
            self, book_schema: BookBase
    ) -> BookModel:
        """Create a new course in the database."""
        book_data = book_schema.model_dump()
        authors: list[AuthorModel] = await self.fetch_author(book_data["author_names"])
        del book_data["author_names"]
        book: BookModel = await self.repo.create_one(book_data)
        await self.repo.add_many_to_many(book, "authors", authors)
        return book

    async def get_all_courses(
            self,
            created_at: dt.datetime | None = None,
            last_id: int | None = None,
            limit: int | None = None,
    ) -> list[BookModel]:
        """
        Retrieve a list of all active book from the database.
        """
        async with self.session.begin():
            books: list[BookModel] | None = await self.repo.get_all(
                created_at=created_at,
                last_id=last_id,
                limit=limit,
            )
        return books if books else []

    async def fetch_author(self, author_names: list) -> list[AuthorModel]:
        authors = await self.author_repo.get_ids_by_lst(author_names)
        if not authors:
            raise AuthorNotExistException()
        return authors

    async def get_book(
            self,
            book_id: int,
    ) -> BookModel:
        """
        Retrieve a book by its ID from the database.
        """
        book: BookModel | None = await self.repo.get_one(
            id=book_id,
        )
        if not book:
            raise BookNotFoundByIdException
        return book

    async def update_course(
            self,
            book_id: int,
            book_fields: BookBase,
    ) -> BookModel:
        """
        Update an existing book by ID and author with the provided fields.
        """
        filtered_books_fields: dict[str, str] = (
            self._validate_schema_for_update_request(book_fields)
        )

        updated_book: BookModel | None = await self.repo.update(
            filtered_books_fields, id=book_id,
        )
        if not updated_book:
            raise BookNotFoundByIdException
        return updated_book

    async def delete_book(
            self,
            book_id: int,
    ) -> None:
        """
        Delete a book in the database.
        """
        deleted_book: BookModel | None = await self.repo.delete(
            id=book_id,
        )
        if not deleted_book:
            raise BookNotFoundByIdException



class AuthorService(BaseService):
    """Service class for handling course-related business logic."""

    def __init__(self, db_session: AsyncSession, repo: AbstractRepository = None):
        super().__init__(db_session)
        self.repo = AuthorRepository()

    async def create_author(
            self, author_schema: AuthorSchema
    ) -> AuthorModel:
        """Create a new book in the database."""
        author_data = author_schema.model_dump()
        author: AuthorModel = await self.repo.create_one(author_data)
        return author