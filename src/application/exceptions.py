from fastapi import HTTPException
from starlette import status


class BaseError(HTTPException):
    ...


class BookNotFoundError(BaseError):
    def __init__(self, detail='Книга не найдена', status_code=status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail=detail)


class AuthorNotFoundError(BaseError):
    def __init__(self, detail='Автор не найден', status_code=status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail=detail)
