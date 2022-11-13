from sqlalchemy import select, update, or_
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.repository.validators import check_model_id_exists
from models.authors import Author
from controllers.authors.schemas import AuthorUpdateRequest


class AuthorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, author_id: int) -> ChunkedIteratorResult:
        stmt = Statements.select_by_id(author_id)
        return await self.session.execute(stmt)

    async def get_list(self, offset: int | None = None, limit: int | None = None,
                       search: str = None) -> ChunkedIteratorResult:
        stmt = Statements.select_all(offset, limit, search)
        return await self.session.execute(stmt)

    async def create(self, author: Author):
        self.session.add(author)

    async def update(self, author: Author, values):
        await self.__check_author_exists(author.id)
        stmt = Statements.update(author, values)
        await self.session.execute(stmt)

    async def delete(self, author: Author):
        await self.session.delete(author)

    @staticmethod
    async def __check_author_exists(author_id: int, raise_exception=True):
        await check_model_id_exists(Author, author_id, raise_exception=raise_exception)


class Statements:

    @classmethod
    def select_by_id(cls, author_id: int):
        return select(Author).where(Author.id == author_id).options(selectinload(Author.books))

    @classmethod
    def select_all(cls, offset=0, limit=1000, search: str = None):
        stmt = select(Author).limit(limit).offset(offset).options(selectinload(Author.books))
        if search:
            stmt = stmt.where(or_(
                Author.name.ilike(f'%{word}%'.strip()) |
                Author.lastname.ilike(f'%{word}%'.strip())
                for word in search.split()
            ))
        return stmt.order_by(Author.id)

    @classmethod
    def update(cls, author: AuthorUpdateRequest, values: dict):
        return update(Author).where(Author.id == author.id).values(values)
