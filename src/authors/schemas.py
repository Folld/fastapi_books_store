from fastapi_utils.api_model import APIModel
from pydantic import Field, validator

from authors.models import Author
from utils.validators import check_model_id_exists


class AuthorCreate(APIModel):
    name: str = Field(example='Sergey')
    lastname: str | None = Field(example='Pushkin')


class AuthorOut(AuthorCreate):
    id: int


class AuthorUpdate(AuthorOut):
    name: str | None = Field(example='Sergey')

    @validator('id')
    def check_author_exists(cls, value):
        check_model_id_exists(Author, value, raise_exception=True)
        return value
