from typing import List

from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from books.schemas import BookCreateRequest, BookOut, BookListResponse, BookUpdateResponse, BookCreateResponse, \
    BookUpdateRequest
from books.services import BookService
from database import get_db
from utils.dependencies import offset_limit_paginator


router = InferringRouter(prefix='/books', tags=['books'])


@cbv(router)
class BooksView:
    session: AsyncSession = Depends(get_db)

    @router.get('/list', status_code=status.HTTP_200_OK)
    async def get_books(self, paginator: dict = Depends(offset_limit_paginator)) -> List[BookListResponse]:
        service = BookService(self.session)
        return await service.get_all(**paginator)

    @router.post('/create', status_code=status.HTTP_201_CREATED)
    async def create_book(self, book: BookCreateRequest) -> BookCreateResponse:
        service = BookService(self.session)
        return await service.create(book)

    @router.patch('/update', status_code=status.HTTP_200_OK, response_model_exclude_none=True)
    async def update_book(self, book: BookUpdateRequest) -> BookUpdateResponse:
        service = BookService(self.session)
        return await service.update(book)
