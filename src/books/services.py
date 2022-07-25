from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from authors.services import AuthorService
from books.models import Book
from books.schemas import BookOut, BookCreate, BookUpdate


class BookService:

    def __init__(self, session: Session):
        self.session = session
        self._author_service = AuthorService(session)

    @property
    def author_service(self):
        return self._author_service

    def create_book(self, book: BookCreate) -> BookOut:
        book_orm = Book(**book.dict())
        self.session.add(book_orm)
        self.session.commit()
        return BookOut.from_orm(book_orm)

    def get_all_books(self, offset: int | None = None, limit: int | None = None):
        query = self.session.query(Book).offset(offset).limit(limit)
        return query.all()

    def update_book(self, book: BookUpdate) -> BookOut:
        books = self.session.query(Book).filter_by(id=book.id)
        books.update(book.dict(exclude_none=True))
        self.session.commit()
        return BookOut.from_orm(books.first())

