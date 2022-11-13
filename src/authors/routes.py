from typing import List
from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from authors.schemas import (
    AuthorCreateResponse, AuthorCreateRequest, AuthorUpdateRequest, AuthorUpdateResponse, AuthorRetrieveResponse
)
from authors.services import AuthorService
from database import get_db
from utils.dependencies import offset_limit_paginator
from utils.responses import Response

router = InferringRouter(prefix='/authors', tags=['authors'])


@cbv(router)
class AuthorsView:
    session: AsyncSession = Depends(get_db)

    @router.get('/{author_id}', status_code=status.HTTP_200_OK)
    async def get(self, author_id: int) -> Response[AuthorRetrieveResponse]:
        service = AuthorService(self.session)
        data = await service.get(author_id)
        return Response(data=data)

    @router.delete('/{author_id}', status_code=status.HTTP_200_OK)
    async def delete(self, author_id: int) -> Response:
        service = AuthorService(self.session)
        await service.delete(author_id)
        return Response(data={})

    @router.get('/', status_code=status.HTTP_200_OK)
    async def get_list(
            self, paginate: dict = Depends(offset_limit_paginator)) -> Response[List[AuthorRetrieveResponse]]:
        service = AuthorService(self.session)
        data = await service.get_list(**paginate)
        return Response(data=data)

    @router.post('/', status_code=status.HTTP_201_CREATED)
    async def create(self, author: AuthorCreateRequest) -> Response[AuthorCreateResponse]:
        service = AuthorService(self.session)
        data = await service.create(author)
        return Response(data=data)

    @router.patch('/', status_code=status.HTTP_200_OK)
    async def update(self, author: AuthorUpdateRequest) -> Response[AuthorUpdateResponse]:
        service = AuthorService(self.session)
        data = await service.update(author)
        return Response(data=data)
