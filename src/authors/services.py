from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from authors.exceptions import AuthorNotFoundError
from authors.models import Author
from authors.schemas import AuthorOut, AuthorCreate, AuthorUpdate
from utils.validators import check_model_id_exists


class AuthorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, author_id: int) -> AuthorOut:
        result = await self.session.get(Author, author_id)
        if not result:
            raise AuthorNotFoundError(f'Author id={author_id} not found')
        return result

    async def get_list(self, offset: int | None = None, limit: int | None = None):
        stmt = Statements.select_all(offset, limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, author: AuthorCreate) -> AuthorOut:
        author_orm = Author(**author.dict())
        self.session.add(author_orm)
        await self.session.commit()
        return AuthorOut.from_orm(author_orm)

    async def update(self, author: AuthorUpdate) -> AuthorOut:
        await self.__check_author_exists(author.id)
        stmt = Statements.update(author)
        await self.session.execute(stmt)
        await self.session.commit()
        return AuthorOut.from_orm(author)

    async def delete(self, author_id: int):
        author = await self.get(author_id)
        await self.session.delete(author)
        await self.session.commit()

    @staticmethod
    async def __check_author_exists(author_id: int, raise_exception=True):
        await check_model_id_exists(Author, author_id, raise_exception=raise_exception)


class Statements:

    @classmethod
    def select_all(cls, offset=0, limit=1000):
        return select(Author).limit(limit).offset(offset).order_by(Author.id)

    @classmethod
    def update(cls, author: AuthorOut):
        return update(Author).where(author.id == author.id).values(author.dict(exclude={'id'}, exclude_none=True))
