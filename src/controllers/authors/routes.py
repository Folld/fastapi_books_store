from typing import List, Type
from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.authors import AuthorService
from controllers.authors.schemas import (
    AuthorCreateResponse, AuthorCreateRequest, AuthorUpdateRequest, AuthorUpdateResponse, AuthorRetrieveResponse
)
from application.database import get_db
from controllers.dependencies import offset_limit_paginator
from controllers.responses import Response

router = InferringRouter(prefix='/authors', tags=['authors'])


@cbv(router)
class AuthorsView:
    _session: AsyncSession = Depends(get_db)
    _service: Type[AuthorService] = AuthorService

    @property
    def session(self):
        return self._session

    @property
    def service(self):
        return self._service(self.session)

    @router.get('/{author_id}', status_code=status.HTTP_200_OK)
    async def get(self, author_id: int) -> Response[AuthorRetrieveResponse]:
        data = await self.service.get_author(author_id)
        return Response(data=data)

    @router.delete('/{author_id}', status_code=status.HTTP_200_OK)
    async def delete(self, author_id: int) -> Response:
        await self.service.delete_author(author_id)
        return Response(data={})

    @router.get('/', status_code=status.HTTP_200_OK)
    async def get_list(
            self, paginate: dict = Depends(offset_limit_paginator)) -> Response[List[AuthorRetrieveResponse]]:
        data = await self.service.get_list(**paginate)
        return Response(data=data)

    @router.post('/', status_code=status.HTTP_201_CREATED)
    async def create(self, author: AuthorCreateRequest) -> Response[AuthorCreateResponse]:
        data = await self.service.create_author(author)
        return Response(data=data)

    @router.patch('/', status_code=status.HTTP_200_OK)
    async def update(self, author: AuthorUpdateRequest) -> Response[AuthorUpdateResponse]:
        data = await self.service.update_author(author)
        return Response(data=data)
