from sqlalchemy.orm import Session

from authors.services import AuthorService
from books.models import Book
from books.schemas import BookDTO


class BookService:

    def __init__(self, session: Session):
        self.session = session
        self._author_service = AuthorService(session)

    @property
    def author_service(self):
        return self._author_service

    def create_book(self, book: BookDTO) -> BookDTO:
        self.author_service.check_author_exists(book.author_id, raise_exception=True)
        book_orm = Book(**book.dict())
        self.session.add(book_orm)
        self.session.commit()
        return BookDTO.from_orm(book_orm)

    def get_all_books(self, offset: int | None = None, limit: int | None = None):
        query = self.session.query(Book).offset(offset).limit(limit)
        return query.all()
