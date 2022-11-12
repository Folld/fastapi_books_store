from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from books.schemas import BookCreateRequest, BookRetrieveResponse, BookUpdateResponse, BookCreateResponse, BookUpdateRequest
from books.services import BookService
from database import get_db
from utils.dependencies import offset_limit_paginator
from utils.responses import Response

router = InferringRouter(prefix='/books', tags=['Books'])


@cbv(router)
class BooksView:
    session: AsyncSession = Depends(get_db)

    @router.get('/list', status_code=status.HTTP_200_OK)
    async def get_list(self, paginator: dict = Depends(offset_limit_paginator)) -> Response[list[BookRetrieveResponse]]:
        service = BookService(self.session)
        data = await service.get_list(**paginator)
        return Response(data=data)

    @router.get('/{book_id}', status_code=status.HTTP_200_OK)
    async def get(self, book_id: int) -> Response[BookRetrieveResponse]:
        service = BookService(self.session)
        data = await service.get(book_id)
        return Response(data=data)

    @router.delete('/{book_id}', status_code=status.HTTP_200_OK)
    async def delete(self, book_id: int) -> Response:
        service = BookService(self.session)
        await service.delete(book_id)
        return Response(data={})

    @router.post('/create', status_code=status.HTTP_201_CREATED)
    async def create(self, book: BookCreateRequest) -> Response[BookCreateResponse]:
        service = BookService(self.session)
        data = await service.create(book)
        return Response(data=data)

    @router.patch('/update', status_code=status.HTTP_200_OK, response_model_exclude_none=True)
    async def update(self, book: BookUpdateRequest) -> Response[BookUpdateResponse]:
        service = BookService(self.session)
        data = await service.update(book)
        return Response(data=data)
