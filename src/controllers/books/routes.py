from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.books import BookService
from controllers.books.schemas import (
    BookCreateRequest, BookRetrieveResponse, BookUpdateResponse, BookCreateResponse, BookUpdateRequest
)
from application.database import get_db
from controllers.dependencies import offset_limit_paginator
from controllers.responses import Response

router = InferringRouter(prefix='/books', tags=['Books'])


@cbv(router)
class BooksView:
    _session: AsyncSession = Depends(get_db)
    _service = BookService

    @property
    def session(self):
        return self._session

    @property
    def service(self):
        return self._service(self.session)

    @router.get('/list', status_code=status.HTTP_200_OK)
    async def get_list(self, paginator: dict = Depends(offset_limit_paginator)) -> Response[list[BookRetrieveResponse]]:
        data = await self.service.get_list(**paginator)
        return Response(data=data)

    @router.get('/{book_id}', status_code=status.HTTP_200_OK)
    async def get(self, book_id: int) -> Response[BookRetrieveResponse]:
        data = await self.service.get_book(book_id)
        return Response(data=data)

    @router.delete('/{book_id}', status_code=status.HTTP_200_OK)
    async def delete(self, book_id: int) -> Response:
        await self.service.delete_book(book_id)
        return Response(data={})

    @router.post('/create', status_code=status.HTTP_201_CREATED)
    async def create(self, book: BookCreateRequest) -> Response[BookCreateResponse]:
        data = await self.service.create_book(book)
        return Response(data=data)

    @router.patch('/update', status_code=status.HTTP_200_OK, response_model_exclude_none=True)
    async def update(self, book: BookUpdateRequest) -> Response[BookUpdateResponse]:
        data = await self.service.update_book(book)
        return Response(data=data)
