from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession

from authors.models import Author
from authors.services import AuthorService
from books.models import Book
from books.schemas import BookOut, BookCreateResponse, BookUpdateResponse, BookUpdateRequest, BookCreateRequest
from utils.validators import check_model_id_exists


class BookService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self._author_service = AuthorService(session)

    @property
    def author_service(self):
        return self._author_service

    async def create(self, book: BookCreateRequest) -> BookCreateResponse:
        await self.__is_author_exists(book.author_id)
        book_orm = Book(**book.dict())
        self.session.add(book_orm)
        await self.session.commit()
        return BookCreateResponse.from_orm(book_orm)

    @staticmethod
    async def __is_author_exists(author_id: int):
        await check_model_id_exists(Author, author_id, raise_exception=True)

    @staticmethod
    async def __is_book_exists(book_id: id):
        await check_model_id_exists(Book, book_id, raise_exception=True)

    async def get_all(self, offset: int | None = None, limit: int | None = None) -> list[Book]:
        stmt = Statements.select_all(offset, limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, book: BookUpdateRequest) -> BookUpdateResponse:
        await self.__is_book_exists(book.id)
        if book.author_id:
            await self.__is_author_exists(book.author_id)
        stmt = Statements.update(book)
        await self.session.execute(stmt)
        await self.session.commit()
        return BookUpdateResponse.from_orm(book)


class Statements:

    @classmethod
    def select_all(cls, offset=0, limit=1000):
        return select(Book).offset(offset).limit(limit).order_by(Book.id)

    @classmethod
    def update(cls, book: BookUpdateRequest):
        return update(Book).where(Book.id == book.id).values(book.dict(exclude={'id'}, exclude_none=True))
