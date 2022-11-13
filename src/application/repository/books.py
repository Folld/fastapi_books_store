from sqlalchemy import select, update
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.repository.validators import check_model_id_exists
from models.authors import Author
from models.books import Book
from controllers.books.schemas import BookUpdateRequest


class BookRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, book: Book):
        await self.__ensure_author_exists(book.author_id)
        self.session.add(book)

    @staticmethod
    async def __ensure_author_exists(author_id: int):
        await check_model_id_exists(Author, author_id, raise_exception=True)

    @staticmethod
    async def __is_book_exists(book_id: id):
        await check_model_id_exists(Book, book_id, raise_exception=True)

    async def get_list(self, offset: int | None = None, limit: int | None = None) -> ChunkedIteratorResult:
        stmt = Statements.select_all(offset, limit)
        return await self.session.execute(stmt)

    async def get(self, book_id: int) -> ChunkedIteratorResult:
        stmt = Statements.select_by_id(book_id)
        return await self.session.execute(stmt)

    async def delete(self, book: Book):
        await self.session.delete(book)

    async def update(self, book: Book, values: dict):
        await self.__is_book_exists(book.id)
        if book.author_id:
            await self.__ensure_author_exists(book.author_id)
        stmt = Statements.update(book, values)
        await self.session.execute(stmt)


class Statements:

    @classmethod
    def select_all(cls, offset=0, limit=1000):
        return select(Book).offset(offset).limit(limit).options(selectinload(Book.author))

    @classmethod
    def select_by_id(cls, book_id: int):
        return select(Book).where(Book.id == book_id).options(selectinload(Book.author))

    @classmethod
    def update(cls, book: BookUpdateRequest, values):
        return update(Book).where(Book.id == book.id).values(values)
