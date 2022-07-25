from fastapi_utils.api_model import APIModel
from pydantic import Field


class AuthorCreate(APIModel):
    name: str = Field(example='Sergey')
    lastname: str | None = Field(example='Pushkin')


class AuthorOut(AuthorCreate):
    id: int


class AuthorUpdate(AuthorOut):
    name: str | None = Field(example='Sergey')
