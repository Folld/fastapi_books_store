from fastapi_utils.api_model import APIModel
from pydantic import Field


class BookDTO(APIModel):
    id: int
    name: str = Field(example='Ring of the King', title='Name of book')
    price: float = 0
    author_id: int | None
