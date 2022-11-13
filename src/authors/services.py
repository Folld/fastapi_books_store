from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from authors.exceptions import AuthorNotFoundError
from authors.models import Author
from authors.schemas import (
    AuthorCreateResponse, AuthorCreateRequest, AuthorRetrieveResponse, AuthorUpdateResponse, AuthorUpdateRequest
)
from utils.validators import check_model_id_exists


class AuthorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, author_id: int) -> AuthorRetrieveResponse:
        stmt = Statements.select_by_id(author_id)
        result = await self.session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound:
            raise AuthorNotFoundError(f'Author id={author_id} not found')

    async def get_list(self, offset: int | None = None, limit: int | None = None) -> AuthorRetrieveResponse:
        stmt = Statements.select_all(offset, limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, author: AuthorCreateRequest) -> AuthorCreateResponse:
        author_orm = Author(**author.dict())
        self.session.add(author_orm)
        await self.session.commit()
        return AuthorCreateResponse.from_orm(author_orm)

    async def update(self, author: AuthorUpdateRequest) -> AuthorUpdateResponse:
        await self.__check_author_exists(author.id)
        stmt = Statements.update(author)
        await self.session.execute(stmt)
        await self.session.commit()
        return AuthorUpdateResponse.from_orm(author)

    async def delete(self, author_id: int):
        author = await self.get(author_id)
        await self.session.delete(author)
        await self.session.commit()

    @staticmethod
    async def __check_author_exists(author_id: int, raise_exception=True):
        await check_model_id_exists(Author, author_id, raise_exception=raise_exception)


class Statements:

    @classmethod
    def select_by_id(cls, author_id: int):
        return select(Author).where(Author.id == author_id).options(selectinload(Author.books))

    @classmethod
    def select_all(cls, offset=0, limit=1000):
        return select(Author).limit(limit).offset(offset).options(selectinload(Author.books)).order_by(Author.id)

    @classmethod
    def update(cls, author: AuthorUpdateRequest):
        update_params = author.dict(exclude={'id'}, exclude_none=True)
        return update(Author).where(author.id == author.id).values(update_params).options(selectinload(Author.books))
