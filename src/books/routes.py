from typing import List

from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from books.schemas import BookDTO
from books.services import BookService
from database import get_db
from utils.dependencies import offset_limit_paginator


router = InferringRouter(prefix='/books', tags=['books'])


@cbv(router)
class BooksView:
    session: Session = Depends(get_db)

    @router.get('/list', response_model=List[BookDTO], response_model_by_alias=True, status_code=status.HTTP_200_OK)
    async def get_books(self, paginator: dict = Depends(offset_limit_paginator)):
        service = BookService(self.session)
        return service.get_all_books(**paginator)

    @router.post('/create')
    async def create_book(self, book: BookDTO):
        service = BookService(self.session)
        return service.create_book(book)
