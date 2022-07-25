from fastapi_utils.api_model import APIModel
from pydantic import Field, validator

from authors.models import Author
from books.models import Book
from utils.validators import check_model_id_exists


class BookCreate(APIModel):
    name: str = Field(example='Ring of the King', title='Name of book')
    price: float = Field(0, example=9.99)
    author_id: int

    @validator('author_id')
    def check_author_exists(cls, value):
        check_model_id_exists(Author, value, raise_exception=True)
        return value


class BookOut(BookCreate):
    id: int


class BookUpdate(BookOut):
    name: str | None = Field(example='Ring of the King', title='Name of book')
    price: float | None = Field(example=9.99)

    @validator('id')
    def validate_id(cls, value):
        check_model_id_exists(Book, value, raise_exception=True)
        return value
