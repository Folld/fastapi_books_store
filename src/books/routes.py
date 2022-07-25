from typing import List

from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from books.schemas import BookCreate, BookOut, BookUpdate
from books.services import BookService
from database import get_db
from utils.dependencies import offset_limit_paginator


router = InferringRouter(prefix='/books', tags=['books'])


@cbv(router)
class BooksView:
    session: Session = Depends(get_db)

    @router.get('/list', status_code=status.HTTP_200_OK)
    async def get_books(self, paginator: dict = Depends(offset_limit_paginator)) -> List[BookOut]:
        service = BookService(self.session)
        return service.get_all_books(**paginator)

    @router.post('/create', status_code=status.HTTP_201_CREATED)
    def create_book(self, book: BookCreate) -> BookOut:
        service = BookService(self.session)
        return service.create_book(book)

    @router.patch('/update', status_code=status.HTTP_200_OK)
    def update_book(self, book: BookUpdate) -> BookOut:
        service = BookService(self.session)
        return service.update_book(book)
