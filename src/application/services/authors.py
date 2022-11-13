from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from application.repository.authors import AuthorRepository
from controllers.authors.schemas import AuthorCreateRequest, AuthorCreateResponse, AuthorUpdateRequest, \
    AuthorUpdateResponse
from models import Author
from application.exceptions import AuthorNotFoundError


class AuthorService:
    _repo_class = AuthorRepository

    def __init__(self, session: AsyncSession):
        self._session = session

    @property
    def session(self):
        return self._session

    @property
    def repo(self):
        return self._repo_class(self.session)

    async def get_list(self, offset: int | None = None, limit: int | None = None) -> list[Author]:
        result = await self.repo.get_list(offset=offset, limit=limit)
        return result.scalars().all()

    async def get_author(self, author_id: int) -> Author:
        result = await self.repo.get(author_id)
        try:
            return result.scalar_one()
        except NoResultFound:
            raise AuthorNotFoundError(f'Автор id={author_id} не найден')

    async def delete_author(self, author_id: int):
        author = await self.get_author(author_id)
        await self.repo.delete(author)
        await self.session.commit()

    async def create_author(self, request: AuthorCreateRequest) -> AuthorCreateResponse:
        author: Author = Author(**request.dict())
        await self.repo.create(author)
        await self.session.commit()
        return AuthorCreateResponse.from_orm(author)

    async def update_author(self, request: AuthorUpdateRequest) -> AuthorUpdateResponse:
        author = Author(**request.dict())
        values = request.dict(exclude={'id'}, exclude_none=True)
        await self.repo.update(author, values)
        await self.session.commit()
        return AuthorUpdateResponse.from_orm(author)
