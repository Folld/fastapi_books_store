from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from application.repository.books import BookRepository
from controllers.books.schemas import BookCreateRequest, BookUpdateRequest, BookCreateResponse, BookUpdateResponse
from models import Book
from application.exceptions import BookNotFoundError


class BookService:
    _repo_class = BookRepository

    def __init__(self, session: AsyncSession):
        self._session = session

    @property
    def session(self):
        return self._session

    @property
    def repo(self):
        return self._repo_class(self.session)

    async def get_list(self, offset: int | None = None, limit: int | None = None) -> list[Book]:
        result = await self.repo.get_list(offset=offset, limit=limit)
        return result.scalars().all()

    async def get_book(self, book_id: int) -> Book:
        result = await self.repo.get(book_id)
        try:
            return result.scalar_one()
        except NoResultFound:
            raise BookNotFoundError(f'Книга id={book_id} не найдена')

    async def delete_book(self, book_id: int):
        book = await self.get_book(book_id)
        await self.repo.delete(book)
        await self.session.commit()

    async def create_book(self, request: BookCreateRequest) -> BookCreateResponse:
        book: Book = Book(**request.dict())
        await self.repo.create(book)
        await self.session.commit()
        return BookCreateResponse.from_orm(book)

    async def update_book(self, request: BookUpdateRequest) -> BookUpdateResponse:
        book = Book(**request.dict())
        values = request.dict(exclude={'id'}, exclude_none=True)
        await self.repo.update(book, values)
        await self.session.commit()
        return BookUpdateResponse.from_orm(book)
