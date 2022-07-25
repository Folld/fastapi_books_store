from typing import List
from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from authors.schemas import AuthorOut, AuthorCreate, AuthorUpdate
from authors.services import AuthorService
from database import get_db
from utils.dependencies import offset_limit_paginator

router = InferringRouter(prefix='/authors', tags=['authors'])


@cbv(router)
class AuthorsView:
    session: Session = Depends(get_db)

    @router.get('/', status_code=status.HTTP_200_OK)
    async def get_authors(self, paginate: dict = Depends(offset_limit_paginator)) -> List[AuthorOut]:
        service = AuthorService(self.session)
        return service.get_all_authors(**paginate)

    @router.post('/', status_code=status.HTTP_201_CREATED)
    def create_author(self, author: AuthorCreate) -> AuthorOut:
        service = AuthorService(self.session)
        return service.create_author(author)

    @router.patch('/', status_code=status.HTTP_200_OK)
    def update_author(self, author: AuthorUpdate) -> AuthorOut:
        service = AuthorService(self.session)
        return service.update_author(author)
