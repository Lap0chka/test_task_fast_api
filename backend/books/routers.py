from __future__ import annotations

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from pydantic import ValidationError
from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from .models import Author, Book, book_authors
from .schemas import BookCreate, BookOut, BookUpdate, ALLOWED_GENRES
# get_async_session должен возвращать AsyncSession (подключение к PostgreSQL)
from core.db import get_async_session  # <-- импортируй свой

router = APIRouter(prefix="/api/v1/books", tags=["books"])

# @router.post(
#     "",
#     status_code=status.HTTP_201_CREATED,
#     response_model=BookOut,
#     description="Add a new book.",
# )
# async def create_book(
#     payload: BookCreate,
#     session: Annotated[AsyncSession, Depends(get_async_session)],
# ) -> BookOut:
#
#     return _book_to_out(book)
#
# @router.get(
#     "",
#     response_model=list[BookOut],
#     description="Retrieve all books with pagination, sorting, and filtering.",
# )
# async def list_books(
#
# ) -> list[BookOut]:
#
#     return [_book_to_out(b) for b in result]
#
# @router.get(
#     "/{book_id}",
#     response_model=BookOut,
#     description="Fetch a specific book by its unique ID.",
# )
# async def get_book(
#     book_id: int,
#     session: Annotated[AsyncSession, Depends(get_async_session)],
# ) -> BookOut:
#
#
# @router.put(
#     "/{book_id}",
#     response_model=BookOut,
#     description="Update an existing book's details.",
# )
# async def update_book(
#     book_id: int,
#     payload: BookUpdate,
#     session: Annotated[AsyncSession, Depends(get_async_session)],
# ) -> BookOut:
#
#
#
# @router.delete(
#     "/{book_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     description="Remove a book from the system.",
# )
# async def delete_book(
#     book_id: int,
#     session: Annotated[AsyncSession, Depends(get_async_session)],
# ) -> None:
#
#
# @router.post(
#     "/bulk-upload",
#     status_code=status.HTTP_201_CREATED,
#     description="Import a collection of books from a JSON file.",
# )
# async def bulk_upload_books(
#     session: Annotated[AsyncSession, Depends(get_async_session)],
#     file: UploadFile = File(..., description="JSON file with an array of books"),
# ):
#     return {"created": len(created_ids), "ids": created_ids, "errors": errors}