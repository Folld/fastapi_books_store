from fastapi_utils.api_model import APIModel
from pydantic import Field


class BaseAuthorModel(APIModel):
    ...


class AuthorBooks(APIModel):
    name: str | None
    price: float | None


class AuthorRetrieveResponse(BaseAuthorModel):
    name: str
    lastname: str | None
    books: list[AuthorBooks]


class AuthorCreateRequest(APIModel):
    name: str = Field(example='Sergey')
    lastname: str | None = Field(example='Pushkin')


class AuthorCreateResponse(BaseAuthorModel):
    id: int


class AuthorUpdateRequest(BaseAuthorModel):
    id: int
    name: str | None = Field(example='Sergey')
    lastname: str | None = Field(example='Pushkin')


class AuthorUpdateResponse(BaseAuthorModel):
    id: int
    name: str | None = Field(example='Sergey')
    lastname: str | None = Field(example='Pushkin')
