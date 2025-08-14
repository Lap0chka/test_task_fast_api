import datetime as dt
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from auth.dependencies import PermissionDependency, get_user_from_jwt
from base.dependencies import get_service
from base.schema import DeleteResponse
from books.models import BookModel
from books.permissions import Is_Authenticated
from books.schemas import BookOutSchema, BookBase, AuthorSchema
from books.services import BookService, AuthorService
from core.settings import API_URL

book_router = APIRouter(
    prefix=f'{API_URL}/books',
    tags=["books"],
    dependencies=[Depends(PermissionDependency([Is_Authenticated]))],
)

author_router = APIRouter(prefix=f'{API_URL}/authors', tags=["authors"])



@book_router.get('/all', response_model=list[BookOutSchema])
async def get_all_books(
        service: Annotated[BookService, Depends(get_service(BookService))],
        created_at: dt.datetime | None = None,
        last_id: int | None = None,
        limit: int | None = None,
) -> list[BookOutSchema] | None:
    """
    Retrieve a list of all available book with optional filtering.
    """
    books: list[BookModel] = await service.get_all_courses(
        created_at, last_id, limit
    )
    return [BookOutSchema.model_validate(c) for c in books]


@book_router.post('/', response_model=BookOutSchema)
async def create_book(
        book_schema: BookBase,
        service: Annotated[BookService, Depends(get_service(BookService))],
) -> BookOutSchema:
    """Endpoint to create a new book."""
    course = await service.create_book(
        book_schema=book_schema
    )
    return BookOutSchema.model_validate(course)


@book_router.get('/{book_id}', response_model=BookOutSchema)
async def get_course(
        book_id: int,
        service: Annotated[BookService, Depends(get_service(BookService))],
) -> BookOutSchema:
    """Endpoint to get a book by its ID."""
    book = await service.get_book(book_id)
    return BookOutSchema.model_validate(book)

@book_router.patch('/{book_id}', response_model=BookOutSchema)
async def update_course(
        book_id: int,
        book_fields: BookBase,
        service: Annotated[BookService, Depends(get_service(BookService))],
) -> BookOutSchema:
    """
    Update an existing book by its ID.
    """
    updated_course = await service.update_book(
        book_id=book_id, book_fields=book_fields
    )
    return BookOutSchema.model_validate(updated_course)


@book_router.delete("/{book_id}", response_model=DeleteResponse)
async def delete_book(
    book_id: int,
    service: Annotated[BookService, Depends(get_service(BookService))],
) -> DeleteResponse:
    await service.delete_book(book_id)
    return DeleteResponse(status="deleted")


@author_router.post('/', response_model=AuthorSchema)
async def create_book(
        author_schema: AuthorSchema,
        service: Annotated[AuthorService, Depends(get_service(AuthorService))],
) -> AuthorSchema:
    """Endpoint to create a new author."""
    author = await service.create_author(
        author_schema=author_schema
    )
    return AuthorSchema.model_validate(author)