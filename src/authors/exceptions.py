from fastapi import status, HTTPException


class BaseError(HTTPException):
    ...


class AuthorNotFoundError(BaseError):
    def __init__(self, detail='Автор не найден', status_code=status.HTTP_404_NOT_FOUND):
        super().__init__(status_code=status_code, detail=detail)
