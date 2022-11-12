from fastapi_utils.api_model import APIModel
from pydantic import Field


class BaseBook(APIModel):
    ...


class BookCreateRequest(BaseBook):
    name: str = Field(example='Ring of the King', title='Name of book')
    price: float = Field(0, example=9.99)
    author_id: int


class BookUpdateRequest(BaseBook):
    id: int
    name: str | None = Field(example='Ring of the King', title='Name of book')
    price: float | None = Field(example=9.99)
    author_id: int | None = Field(example=9.99)


class BookOut(BaseBook):
    id: int

    class Config:
        orm_mode = True


class BookCreateResponse(BookOut):
    ...


class BookUpdateResponse(BookOut):
    name: str | None = Field(example='Ring of the King', title='Name of book')
    price: float | None = Field(example=9.99)
    author_id: int | None = Field(example=9.99)


class BookListResponse(BookOut):
    name: str | None
    price: str | None
    author_id: int | None
